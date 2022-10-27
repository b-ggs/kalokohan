from django.core.exceptions import ImproperlyConfigured
from django.http.request import HttpRequest
from ninja.security import HttpBearer

from kalokohan.configs.models import SiteConfiguration


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        if not (api_key := SiteConfiguration.get_solo().api_key):
            raise ImproperlyConfigured("API key is not set")

        if token == api_key:
            return token
