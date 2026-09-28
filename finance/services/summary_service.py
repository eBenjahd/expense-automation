from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import F

from finance.models import Transaction
from finance.utils import get_week_range, get_month_range


def weekly_summary(user):

    reference_date = timezone.localtime()
    start, end = get_week_range(reference_date)

    transaction = (
        Transaction.objects
        .filter(
            user=user,
            kind="expense",
        )
        .annotate(
            effective_date=Coalesce(
                "occurred_at",
                "created_at",
            )
        )
        .filter(
            effective_date__gte=start,
            effective_date__lt=end,
        )
    )

    total = (
        transaction
        .aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    by_category = (
        transaction
        .values(
            category_name=F("category__name")
        )
        .annotate(
            total=Sum("amount")
        )
    )

    return {
        "total_spent": total,
        "by_category": list(by_category),
    }


def monthly_summary(user, category, start_month=None):

    if start_month is None:
        start_month = timezone.localtime()

    start, end = get_month_range(
        reference_date=start_month
    )

    transaction = (
        Transaction.objects
        .filter(
            user=user,
            kind="expense",
        )
        .annotate(
            effective_date=Coalesce(
                "occurred_at",
                "created_at",
            )
        )
        .filter(
            effective_date__gte=start,
            effective_date__lt=end,
        )
    )

    if category:

        transaction = transaction.filter(
            category__name=category,
        )

        total = (
            transaction
            .aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        return {
            "category": category,
            "total": total,
        }

    total = (
        transaction
        .aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    by_category = (
        transaction
        .values(
            category_name=F("category__name")
        )
        .annotate(
            total=Sum("amount")
        )
    )

    return {
        "total_spent": total,
        "by_category": list(by_category),
    }