from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from finance.serializers import BudgetSerializer
from finance.models import Budget
from users.models import TelegramProfile

class BudgetListCreateView(ListCreateAPIView):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        telegram_chat_id = self.request.headers.get("X-Telegram-Chat-ID")

        profile = TelegramProfile.objects.select_related("user").get(
            telegram_chat_id=telegram_chat_id
        )

        return Budget.objects.filter(user=profile.user)

    def perform_create(self, serializer):
        telegram_chat_id = self.request.headers.get("X-Telegram-Chat-ID")

        profile = TelegramProfile.objects.select_related("user").get(
            telegram_chat_id=telegram_chat_id
        )

        serializer.save(user=profile.user)


class BudgetDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        telegram_chat_id = self.request.headers.get("X-Telegram-Chat-ID")

        profile = TelegramProfile.objects.select_related("user").get(
            telegram_chat_id=telegram_chat_id
        )

        return Budget.objects.filter(user=profile.user)