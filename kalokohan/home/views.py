import platform

from django.utils.version import get_complete_version
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context |= {
            "python_version": ".".join(platform.python_version_tuple()),
            "django_version": ".".join(str(item) for item in get_complete_version()),
        }
        return context
