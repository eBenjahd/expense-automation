from django.urls import path
from users.views import TelegramUserView,TelegramProfileView

urlpatterns = [
    path('create/user/',TelegramUserView.as_view(), name='create_user'),
    path('profile/',TelegramProfileView.as_view(), name='profile_identify'),
] 