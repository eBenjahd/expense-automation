from rest_framework.views import APIView
from expense.permissions import IsN8NTelegramRequest
from finance.services import MonthlyReportService
from users.models import TelegramProfile
from django.utils import timezone
from django.http import FileResponse


class MonthlyReportView(APIView):

    permission_classes = [IsN8NTelegramRequest]

    def get(self, request):

        telegram_user_id = request.headers.get("X-Telegram-Chat-ID")

        profile = TelegramProfile.objects.select_related(
            "user"
        ).get(
            telegram_chat_id=telegram_user_id
        )

        user = profile.user

        reference_date = timezone.localtime()

        year = request.query_params.get(
            "year",
            reference_date.year,
        )

        month = request.query_params.get(
            "month",
            reference_date.month,
        )

        report = MonthlyReportService(
            user=user,
            year=int(year),
            month=int(month),
        )

        file_path = report.generate_excel()

        return FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            filename="monthly_report.xlsx",
            content_type=(
                "application/vnd.openxmlformats-officedocument"
                ".spreadsheetml.sheet"
            ),
        )