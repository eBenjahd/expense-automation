from datetime import timedelta
from django.utils import timezone


def get_week_range(reference_date=None):
    
    date = reference_date or timezone.now()

    weekday = date.weekday()

    start_date = date - timedelta(days=weekday)

    end_date = start_date + timedelta(days=7)

    return start_date, end_date

