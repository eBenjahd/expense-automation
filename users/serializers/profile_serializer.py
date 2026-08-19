from rest_framework import serializers
from users.models import TelegramProfile

class TelegramProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramProfile
        fields = [
            "telegram_chat_id",
            "telegram_username",
        ]