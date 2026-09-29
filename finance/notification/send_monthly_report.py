import requests

from django.conf import settings


def send_monthly_report(user, file_path, year, month):

    from users.models import TelegramProfile

    profile = TelegramProfile.objects.get(
        user=user
    )

    filename = (
        f"reporte_financiero_"
        f"{year}_{month:02d}.xlsx"
    )

    with open(file_path, "rb") as file:

        response = requests.post(
            settings.N8N_EXPENSES_EVENTS_URL,
            data={
                "event": "monthly_report",
                "telegram_chat_id": profile.telegram_chat_id,
                "year": str(year),
                "month": str(month),
            },
            files={
                "file": (
                    filename,
                    file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
            },
            timeout=30,
        )

    response.raise_for_status()