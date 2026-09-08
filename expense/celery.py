import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "expense.settings",
)

app = Celery("expense")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

app.autodiscover_tasks()
app.conf.timezone = "America/Lima"

app.conf.beat_schedule = {
    "weekly-summary-every-sunday": {
        "task": "finance.tasks.weekly.weekly_summary_task",
        "schedule": crontab(
            day_of_week="sunday",
            hour=20,
            minute=0,
        ),
    },
}

# PRUEBA DESARROLLO PARA COMPROBAR FUNCIONAMIENTO
# app.conf.beat_schedule = {
#     "weekly-summary-every-minute": {
#         "task": "finance.tasks.test.weekly_summary_task",
#         "schedule": crontab(minute="*"),
#     },
# }