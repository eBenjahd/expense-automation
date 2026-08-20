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

        category = self.request.query_params.get('category')
        kind = self.request.query_params.get('kind')
        account = self.request.query_params.get('account')
        currency = self.request.query_params.get('currency')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        amount_min = self.request.query_params.get('amount_min')
        amount_max = self.request.query_params.get('amount_max')

        telegram_chat_id = self.request.headers.get(
            "X-Telegram-Chat-ID"
        )

        profile = TelegramProfile.objects.select_related(
            "user"
        ).get(
            telegram_chat_id=telegram_chat_id
        )

        queryset = Transaction.objects.filter(user=profile.user)

        if category:
            queryset = queryset.filter(category__name=category)
        
        if kind:
            queryset = queryset.filter(kind=kind)

        if account:
            queryset = queryset.filter(account__name=account)
        
        if currency:
            queryset = queryset.filter(currency=currency)

        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)

        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        if amount_min:
            queryset = queryset.filter(amount__gte=amount_min)

        if amount_max:
            queryset = queryset.filter(amount__lte=amount_max)

        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):

        telegram_chat_id = self.request.headers.get(
            "X-Telegram-Chat-ID"
        )

        profile = TelegramProfile.objects.select_related("user").get(
            telegram_chat_id=telegram_chat_id
        )

        serializer.save(
            user=profile.user,
            raw_text=self.request.data.get('raw_text',''),
            source = 'telegram',
        )


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