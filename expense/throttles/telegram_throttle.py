from rest_framework.throttling import SimpleRateThrottle


class TelegramSecondThrottle(SimpleRateThrottle):

    scope = "telegram_second"

    def get_cache_key(self, request, view):

        chat_id = request.headers.get("X-Telegram-Chat-ID")

        if chat_id:
            ident = f"telegram:{chat_id}"
        else:
            ident = "n8n:unknown"

        return f"throttle:{self.scope}:{ident}"


class TelegramMinuteThrottle(SimpleRateThrottle):

    scope = "telegram_minute"

    def get_cache_key(self, request, view):

        chat_id = request.headers.get("X-Telegram-Chat-ID")

        if chat_id:
            ident = f"telegram:{chat_id}"
        else:
            ident = "n8n:unknown"

        return f"throttle:{self.scope}:{ident}"
    

class N8NThrottle(SimpleRateThrottle):

    scope = "n8n"

    def get_cache_key(self, request, view):

        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return None

        return f"throttle:n8n:{api_key}"
    

class TelegramDayThrottle(SimpleRateThrottle):

    scope = "telegram_day"

    def get_cache_key(self, request, view):

        chat_id = request.headers.get("X-Telegram-Chat-ID")

        if chat_id:
            ident = f"telegram:{chat_id}"
        else:
            ident = "n8n:unknown"

        return f"throttle:{self.scope}:{ident}"