from django.conf import settings
from rest_framework.permissions import BasePermission
from users.models import TelegramProfile

class IsN8NTelegramRequest(BasePermission):

    def has_permission(self, request, view):
        
        n8n_api_key = request.headers.get('X-API-Key')
        user_id = request.headers.get('X-Telegram-Chat-ID')

        if not n8n_api_key or n8n_api_key != settings.N8N_API_KEY:
            return False

        if not user_id:
            return False
        
        try:
            profile = TelegramProfile.objects.select_related(
                "user"
            ).get(
                telegram_chat_id=user_id
            )
        except TelegramProfile.DoesNotExist:
            return False

        request.telegram_profile = profile
        request.telegram_user = profile.user

        return True