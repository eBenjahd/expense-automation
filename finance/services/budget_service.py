from django.db.models import Sum
from django.db.models.functions import Coalesce

from finance.models import Budget, Transaction
from finance.utils import get_month_range


ALERT_WARNING = "warning"
ALERT_REACHED = "reached"
ALERT_NONE = None


def check_budget(transaction):

    if transaction.kind != "expense" or transaction.category is None:
        return None

    budget = Budget.objects.filter(
        user=transaction.user,
        category=transaction.category,
        currency=transaction.currency,
    ).first()

    if not budget:
        return None

    if budget.monthly_limit <= 0:
        return None

    reference_date = transaction.occurred_at or transaction.created_at
    start, end = get_month_range(reference_date)

    total_spent = (
        Transaction.objects
        .filter(
            user=transaction.user,
            category=transaction.category,
            currency=transaction.currency,
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

    percentage = float(total_spent) / float(budget.monthly_limit)

    if percentage >= 1.0:
        level = ALERT_REACHED
    elif percentage >= 0.8:
        level = ALERT_WARNING
    else:
        level = ALERT_NONE

    if level is None:
        return {
            "budget": budget,
            "total_spent": total_spent,
            "limit": budget.monthly_limit,
            "percentage": round(percentage * 100, 1),
            "level": level,
            "should_notify": False,
            "period_start": start,
            "period_end": end,
        }

    same_period = budget.last_alert_period == start.date()

    already_notified_this_level = (
        same_period
        and budget.last_alert_level == level
    )

    already_maxed_out = (
        same_period
        and budget.last_alert_level == ALERT_REACHED
    )

    should_notify = (
        not already_notified_this_level
        and not already_maxed_out
    )

    if should_notify:
        budget.last_alert_level = level
        budget.last_alert_period = start.date()

        budget.save(
            update_fields=[
                "last_alert_level",
                "last_alert_period",
            ]
        )

    return {
        "budget": budget,
        "total_spent": total_spent,
        "limit": budget.monthly_limit,
        "percentage": round(percentage * 100, 1),
        "level": level,
        "should_notify": should_notify,
        "period_start": start,
        "period_end": end,
    }