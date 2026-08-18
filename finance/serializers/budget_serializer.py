from rest_framework import serializers
from finance.models import Budget, Category
from finance.serializers import CategorySerializer

class BudgetSerializer(serializers.ModelSerializer):

    category = CategorySerializer()

    class Meta:

        model = Budget
        fields = ["id","category", "monthly_limit", "currency"]
        read_only_fields = ["id"]

    def create(self, validated_data):

        category_data = validated_data.pop("category", None)
        user = validated_data.pop("user")

        if category_data:

            category_name = category_data["name"].strip().lower()
            category_kind = category_data["kind"]

            category, _ = Category.objects.get_or_create(
                user=user,
                name=category_name,
                kind=category_kind
            )
        else:
            category = None

        return Budget.objects.create(
            user=user,
            category=category,
            **validated_data
        )