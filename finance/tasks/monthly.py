from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone

from finance.services import MonthlyReportService
from finance.notification import send_monthly_report


@shared_task
def monthly_report_task():

    today = timezone.localtime()

    if today.month == 1:
        year = today.year - 1
        month = 12
    else:
        year = today.year
        month = today.month - 1

    users = User.objects.filter(
        telegramprofile__isnull=False
    )

    reports_sent = 0

    for user in users:

        report = MonthlyReportService(
            user=user,
            year=year,
            month=month,
        )

        file_path = report.generate_excel()

        send_monthly_report(
            user=user,
            file_path=file_path,
            year=year,
            month=month,
        )

        reports_sent += 1

    return {
        "event": "monthly_report",
        "data": {
            "year": year,
            "month": month,
            "reports_sent": reports_sent,
        },
    }