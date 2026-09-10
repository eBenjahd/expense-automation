from django.test import TestCase
from django.contrib.auth.models import User

from finance.serializers import BudgetSerializer
from finance.models import Budget, Category


class BudgetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

    def test_budget_creation(self):
        data = {
            "category": {
                "name": "Comida",
                "kind": "expense",
            },
            "monthly_limit": 200,
            "currency": "PEN",
        }

        serializer = BudgetSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        budget = serializer.save(user=self.user)

        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.monthly_limit, 200)
        self.assertEqual(budget.currency, "PEN")
        self.assertEqual(budget.category.name, "comida")
        self.assertEqual(budget.category.kind, "expense")

    def test_is_monthly_limit_not_null(self):

        data = {
            "category": {
                "name": "Comida",
                "kind": "expense",
            },
            "currency": "PEN",
        }

        serializer = BudgetSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("monthly_limit", serializer.errors)

        # print ("""\n""")

        # print(f'Errores del serializer: {serializer.errors}')

    def test_is_monthly_limit_lower_than_zero(self):

        data = {
            "category": {
                "name": "Comida",
                "kind": "expense",
            },
            "monthly_limit": -299,
            "currency": "PEN",
        }

        serializer = BudgetSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("monthly_limit", serializer.errors)
        self.assertEqual(
            str(serializer.errors["monthly_limit"][0]),
            "El presupuesto no puede ser negativo."
        )

        # print(serializer.errors)

    def test_budget_uses_exists_category(self):

        budget = Category.objects.create(
            user=self.user,
            name="comida",
            kind="expense",
        )

        # print(f"Creacion budget: {budget}")

        data = {
            "category": {
                "name": "Comida",
                "kind": "expense",
            },
            "monthly_limit": 200,
            "currency": "PEN",
        }

        serializer = BudgetSerializer(data = data) 

        self.assertTrue(serializer.is_valid())

        budget = serializer.save(user=self.user) # very important to save
        # print(serializer.data)
        # print(f'Budget -> {budget}')

        budget_category_count = Category.objects.count()
        # print(f'Count: {budget_category_count}')

        self.assertEqual(budget_category_count, 1)
        self.assertEqual(budget.category.name, "comida")
        self.assertEqual(budget.category.kind, "expense")

    def test_category_name_is_normalized(self):

        data = {
            "category": {
                "name": "   COMIDA   ",
                "kind": "expense",
            },
            "monthly_limit": 200,
            "currency": "PEN",
        }

        serializer = BudgetSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        budget = serializer.save(user=self.user)

        # print("Nombre enviado:", data["category"]["name"])
        # print("Nombre guardado:", budget.category.name)

        self.assertEqual(budget.category.name, "comida")