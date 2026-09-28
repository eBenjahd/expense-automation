from rest_framework.views import APIView
from rest_framework.response import Response

from expense.permissions import IsN8NTelegramRequest

from users.models import TelegramProfile
from finance.services import monthly_summary

from django.utils import timezone


class SummaryView(APIView):

    POSSIBLE_OPTIONS = ["weekly","monthly", "yearly"]

    permission_classes = [IsN8NTelegramRequest]

    def get(self, request):

        rango = request.query_params.get("range")
        category_name = request.query_params.get("category")
        month = request.query_params.get("month")

        telegram_user_id = request.headers.get(
            "X-Telegram-Chat-ID"
        )

        if rango not in self.POSSIBLE_OPTIONS:

            return Response({
                "user_id" : telegram_user_id,
                "error" : "Invalid range option."
            }, status=400)
        
        
        if month:
            
            month = int(month)

            if month < 1 or month > 12:
                return Response({
                    "user_id": telegram_user_id,
                    "error": "Month must be between 1 and 12."
                }, status=400)

            reference_date = timezone.localtime()
            start_month = reference_date.replace(
                month=month,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        else:
            start_month = None


        if category_name:
            category_name = category_name.lower()

        profile = TelegramProfile.objects.select_related("user").get(
            telegram_chat_id=telegram_user_id
        )

        user = profile.user


        match rango:

            case "weekly":
                ...

            case "monthly":
                summary = monthly_summary(
                    user=user,
                    category=category_name,
                    start_month=start_month,
                )
            
            case "yearly":
                ...


        return Response({
            "user_id": telegram_user_id,
            "range": rango,
            **summary,
        })