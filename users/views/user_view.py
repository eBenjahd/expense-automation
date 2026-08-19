from rest_framework.generics import CreateAPIView, RetrieveAPIView
from users.serializers import TelegramSerializer, TelegramProfileSerializer
from expense.permissions import IsN8NRequest
from django.shortcuts import get_object_or_404
from users.models import TelegramProfile

class TelegramUserView(CreateAPIView):

    serializer_class = TelegramSerializer
    permission_classes = [IsN8NRequest]


class TelegramProfileView(RetrieveAPIView):

    serializer_class = TelegramProfileSerializer
    permission_classes = [IsN8NRequest]

    def get_object(self):

        chat_id = self.request.headers.get(
            "X-Telegram-Chat-ID"
        )

        return get_object_or_404(
            TelegramProfile,
            telegram_chat_id=chat_id
        )