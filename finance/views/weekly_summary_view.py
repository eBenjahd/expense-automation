from rest_framework.views import APIView
from rest_framework.response import Response
from finance.services import weekly_summary
from expense.permissions import IsN8NTelegramRequest
from expense.throttles import TelegramMinuteThrottle, TelegramDayThrottle

class WeeklySummaryView(APIView):
    permission_classes = [IsN8NTelegramRequest]
    throttle_classes = [TelegramMinuteThrottle, TelegramDayThrottle]

    def get(self, request):
        total = weekly_summary(request.telegram_user)

        return Response({
            "total_spent": total
        })