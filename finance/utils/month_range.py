from django.utils import timezone

def get_month_range(reference_date=None):
    """Devuelve (inicio, fin_exclusivo) del mes de reference_date."""
    ref = reference_date or timezone.now()
    start = ref.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)

    return start, end