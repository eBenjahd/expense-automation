from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import TelegramProfile

class TelegramSerializer(serializers.ModelSerializer):

    class Meta:

        model = TelegramProfile 
        fields = ["telegram_chat_id", "telegram_username"]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=f"telegram_{validated_data['telegram_chat_id']}"
        )

        return TelegramProfile.objects.create(
            user=user,
            **validated_data
        )