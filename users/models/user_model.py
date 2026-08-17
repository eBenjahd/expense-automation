from django.db import models
from django.contrib.auth.models import User

class TelegramProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_chat_id = models.BigIntegerField(unique=True, db_index=True)
    telegram_username = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.telegram_username