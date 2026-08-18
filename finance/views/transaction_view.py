from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from finance.serializers import TransactionSerializer
from finance.models import Transaction
from users.models import TelegramProfile

class TransactionListCreateView(ListCreateAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):

        telegram_chat_id = self.request.headers.get(
            "X-Telegram-Chat-ID"
        )

        profile = TelegramProfile.objects.select_related(
            "user"
        ).get(
            telegram_chat_id=telegram_chat_id
        )

        return Transaction.objects.filter(
            user=profile.user
        )
    
    def perform_create(self, serializer):

        telegram_chat_id = self.request.headers.get(
            "X-Telegram-Chat-ID"
        )

        profile = TelegramProfile.objects.select_related("user").get(
            telegram_chat_id=telegram_chat_id
        )

        serializer.save(user=profile.user)


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    
    serializer_class = TransactionSerializer

    def get_queryset(self):

        telegram_chat_id = self.request.headers.get(
            "X-Telegram-Chat-ID"
        )

        profile = TelegramProfile.objects.select_related(
            "user"
        ).get(
            telegram_chat_id=telegram_chat_id
        )

        return Transaction.objects.filter(
            user=profile.user
        )