from django.urls import path
from .views import (
    TransactionListCreateView,
    TransactionDetailView,
    BudgetListCreateView,
    BudgetDetailView,
    WeeklySummaryView,
    SummaryView,
    MonthlyReportView,
)

urlpatterns = [
    path("transactions/", TransactionListCreateView.as_view(), name="transaction-list-create",),
    path("transactions/<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail",),
    path("budgets/", BudgetListCreateView.as_view(), name="budgets-list-create"),
    path("budgets/<int:pk>/", BudgetDetailView.as_view(), name="budgets-detail"),
    path("summary/weekly/", WeeklySummaryView.as_view(), name="weekly-summary"),
    path("summary/", SummaryView.as_view(), name="monthly-summary"),
    path("reports/excel/", MonthlyReportView.as_view(), name="excel-report"),
]