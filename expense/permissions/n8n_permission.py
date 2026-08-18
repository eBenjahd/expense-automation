from expense import settings
from rest_framework.permissions import BasePermission

class IsN8NRequest(BasePermission):

    def has_permission(self, request, view):\
    
        n8n_api_key = request.headers.get('X-API-Key')

        return (
            n8n_api_key is not None
            and n8n_api_key == settings.N8N_API_KEY
        )