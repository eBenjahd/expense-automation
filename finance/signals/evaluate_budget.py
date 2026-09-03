from django.db.models.signals import post_save
from django.dispatch import receiver

from finance.models import Transaction
from finance.services.budget_service import check_budget
from finance.notification import send_budget_notification


@receiver(post_save, sender=Transaction)
def evaluate_budget(sender, instance, created, **kwargs):

    if not created:
        return

    result = check_budget(instance)

    if result and result["should_notify"]:
        send_budget_notification(result)