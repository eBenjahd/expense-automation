import pandas as pd

from django.utils import timezone
from django.db.models.functions import Coalesce

from finance.models import Transaction, Budget
from finance.utils import get_month_range

class MonthlyReportService:

    def __init__(self, user, year=None, month=None):

        self.user = user
        reference_date = timezone.localtime()

        if year is not None:
            reference_date = reference_date.replace(year=year)

        if month is not None:
            reference_date = reference_date.replace(month=month)

        self.start, self.end = get_month_range(reference_date)

    def generate_excel(self):

        expenses = self.analyze_expense()
        incomes = self.analyze_income()
        budgets = self.get_budgets()
        accounts = self.get_accounts()

    def analyze_expense(self):

        expenses = (
            Transaction.objects
            .filter(
                user=self.user,
                kind="expense",
            )
            .annotate(
                effective_date=Coalesce(
                    "occurred_at",
                    "created_at",
                )
            )
            .filter(
                effective_date__gte=self.start,
                effective_date__lt=self.end,
            )
            .values(
                "amount",
                "category__name",
                "account__name",
                "currency",
            )
        )

        df = pd.DataFrame.from_records(expenses)

        return df
    
    def analyze_income(self):

        incomes = ( 
            Transaction.objects.filter(
                user=self.user,
                kind= "income"
            )
            .annotate(
                effective_date=Coalesce(
                    "occurred_at",
                    "created_at",
                )
            )
            .filter(
                effective_date__gte=self.start,
                effective_date__lt=self.end,
            )
            .values(
                "amount",
                "category__name",
                "account__name",
                "currency",
            )
        )

        df = pd.DataFrame.from_records(incomes)

        return df
    

    def get_budgets(self):

        budgets = (
            Budget.objects.filter(
                user=self.user
            ).values(
                "category__name",
                "monthly_limit",
                "currency"
            )
        )

        df = pd.DataFrame.from_records(budgets)

        return df
    
    def get_accounts(self):

        accounts = (
            Transaction.objects
            .filter(
                user=self.user,
            )
            .annotate(
                effective_date=Coalesce(
                    "occurred_at",
                    "created_at",
                )
            )
            .filter(
                effective_date__gte=self.start,
                effective_date__lt=self.end,
            )
            .values(
                "account__name",
                "currency",
            )
        )

        df = pd.DataFrame.from_records(accounts)

        return df