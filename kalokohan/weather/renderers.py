from typing import Any

from django.http import HttpRequest
from ninja.renderers import BaseRenderer
from prometheus_client import CONTENT_TYPE_LATEST


class PrometheusMetricsRenderer(BaseRenderer):
    media_type = CONTENT_TYPE_LATEST

    def render(
        self,
        request: HttpRequest,
        data: Any,
        *,
        response_status: int,
    ) -> str | None:
        if isinstance(data, bytes):
            return data.decode("utf-8")
        return "Response is intentionally empty"
