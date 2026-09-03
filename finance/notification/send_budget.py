import requests
from django.conf import settings

from users.models import TelegramProfile


def send_budget_notification(result):
    budget = result["budget"]

    profile = TelegramProfile.objects.get(
        user=budget.user
    )

    response = requests.post(
        settings.N8N_EXPENSES_EVENTS_URL,
        json={
            "event": "budget_alert",
            "data": {
                "telegram_chat_id": profile.telegram_chat_id,
                "category": budget.category.name,
                "currency": budget.currency,
                "total_spent": str(result["total_spent"]),
                "limit": str(result["limit"]),
                "percentage": result["percentage"],
                "level": result["level"],
            },
        },
        timeout=5,
    )