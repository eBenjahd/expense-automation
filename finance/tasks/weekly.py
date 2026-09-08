from celery import shared_task
from django.contrib.auth.models import User

from finance.services.summary_service import weekly_summary
from finance.notification import send_weekly_summary


@shared_task
def weekly_summary_task():

    users = User.objects.filter(
        telegramprofile__isnull=False
    )

    for user in users:

        summary = weekly_summary(user)  
        send_weekly_summary(
            user,
            summary,
        )

    return "OK"