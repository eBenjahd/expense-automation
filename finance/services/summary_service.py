from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import Coalesce

from finance.models import Transaction
from finance.utils import get_week_range


def weekly_summary(user):

    reference_date = timezone.now()
    start, end = get_week_range(reference_date)

    summary = (
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
        .aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    return summary