from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http.request import HttpRequest
from ninja.security import HttpBearer


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        if not (
            hasattr(settings, "WALLPAPERS_API_KEY") and settings.WALLPAPERS_API_KEY
        ):
            raise ImproperlyConfigured("API key is not set")

        if token == settings.WALLPAPERS_API_KEY:
            return token
