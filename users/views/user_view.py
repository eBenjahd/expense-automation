from rest_framework.generics import CreateAPIView
from users.serializers import TelegramSerializer
from expense.permissions import IsN8NRequest

class TelegramUserView(CreateAPIView):

    serializer_class = TelegramSerializer
    permission_classes = [IsN8NRequest]
