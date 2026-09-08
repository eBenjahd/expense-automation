import requests
from django.conf import settings


def send_weekly_summary(user, summary):

    from users.models import TelegramProfile

    profile = TelegramProfile.objects.get(
        user=user
    )

    response = requests.post(
        settings.N8N_EXPENSES_EVENTS_URL,
        json={
            "event": "weekly_summary",
            "data": {
                "telegram_chat_id": profile.telegram_chat_id,
                "total_spent": str(summary["total_spent"]),
                "by_category": [
                    {
                        "category": item["category_name"],
                        "total": str(item["total"]),
                    }
                    for item in summary["by_category"]
                ],
            },
        },
        timeout=5,
    )

    response.raise_for_status()