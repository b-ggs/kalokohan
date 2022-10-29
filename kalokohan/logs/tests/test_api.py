from django.test import TestCase
from django.urls import reverse
from faker import Faker

from kalokohan.configs.models import SiteConfiguration
from kalokohan.logs.models import LogItem, LogSource, LogType

fake = Faker()


class TestLog(TestCase):
    def setUp(self) -> None:
        self.url = reverse("api-1.0.0:log")

        site_config = SiteConfiguration.get_solo()
        site_config.api_key = "api_key"  # pragma: allowlist secret
        site_config.save()

    def test_auth_required(self) -> None:
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, 401)

        resp = self.client.post(
            self.url,
            data={},
            HTTP_Authorization="Bearer fake_api_key",
        )
        self.assertEqual(resp.status_code, 401)

        resp = self.client.post(
            self.url,
            data={},
            HTTP_Authorization="Bearer api_key",
        )
        self.assertEqual(resp.status_code, 400)

    def test_log_created(self) -> None:
        log_type = fake.random_element(LogType.values)
        log_source = fake.random_element(LogSource.values)
        message = fake.sentence()

        resp = self.client.post(
            self.url,
            data={
                "log_type": log_type,
                "log_source": log_source,
                "message": message,
            },
            content_type="application/json",
            HTTP_Authorization="Bearer api_key",
        )

        self.assertEqual(resp.status_code, 200)

        uuid = resp.json()["uuid"]
        log_item = LogItem.objects.get(uuid=uuid)

        self.assertEqual(log_item.log_type, log_type)
        self.assertEqual(log_item.log_source, log_source)
        self.assertEqual(log_item.message, message)

    def test_invalid(self) -> None:
        log_type = "FAKE"
        log_source = "FAKE"
        message = "FAKE"

        before_count = LogItem.objects.count()

        resp = self.client.post(
            self.url,
            data={
                "log_type": log_type,
                "log_source": log_source,
                "message": message,
            },
            content_type="application/json",
            HTTP_Authorization="Bearer api_key",
        )

        self.assertEqual(resp.status_code, 422)
        self.assertEqual(LogItem.objects.count(), before_count)
