from django.urls import path
from users.views import TelegramUserView

urlpatterns = [
    path('create/user/',TelegramUserView.as_view(), name='create_user'),
] 