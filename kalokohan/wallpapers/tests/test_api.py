import responses
from django.test import TestCase, override_settings
from django.urls import reverse

from kalokohan.wallpapers.clients import get_litterbox_client, get_unsplash_client


@override_settings(
    WALLPAPERS_API_KEY="wallpapers",  # pragma: allowlist secret
    WALLPAPERS_UNSPLASH_CLIENT_CLASS="kalokohan.wallpapers.clients.UnsplashClient",
    WALLPAPERS_UNSPLASH_ACCESS_ID="unsplash_access_id",
    WALLPAPERS_LITTERBOX_CLIENT="kalokohan.wallpapers.clients.LitterboxClient",
)
class GetWallpaperTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse("api-1.0.0:get_wallpaper")

        responses.start()
        self.setupResponses()

    def tearDown(self) -> None:
        responses.stop()

    def setupResponses(self) -> None:
        self.fake_image_url = "http://fakeimage.com/asdf.jpg"
        self.fake_item_url = "http://fakeimage.com/asdf/"
        self.fake_litterbox_url = "http://litterbox.fake/asdf.jpg"

        unsplash_base_url = get_unsplash_client().base_url
        responses.add(
            responses.GET,
            f"{unsplash_base_url}/photos/random",
            headers={
                "Accept-Version": "v1",
                "Authorization": "Client-ID unsplash_access_id",
            },
            json={
                "urls": {"full": self.fake_image_url},
                "links": {"html": self.fake_item_url},
            },
        )

        fake_image_binary = "fake_image_binary"
        responses.add(
            responses.GET,
            self.fake_image_url,
            body=fake_image_binary,
        )

        litterbox_base_url = get_litterbox_client().base_url
        files = {
            "reqtype": (None, "fileupload"),
            "time": (None, "1h"),
            "fileToUpload": ("image.jpg", fake_image_binary.encode()),
        }
        responses.add(
            responses.POST,
            litterbox_base_url,
            match=[responses.matchers.multipart_matcher(files)],
            body=self.fake_litterbox_url.encode(),
        )

    def test_response(self) -> None:
        resp = self.client.get(
            self.url,
            HTTP_Authorization="Bearer wallpapers",
        )

        self.assertEqual(resp.status_code, 200)

        resp_json = resp.json()
        self.assertEqual(resp_json["image_url"], self.fake_image_url)
        self.assertEqual(resp_json["item_url"], self.fake_item_url)
        self.assertEqual(resp_json["litterbox_url"], self.fake_litterbox_url)

    def test_auth_required(self) -> None:
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

        resp = self.client.get(
            self.url,
            HTTP_Authorization="Bearer fake_api_key",
        )
        self.assertEqual(resp.status_code, 401)

        resp = self.client.get(
            self.url,
            HTTP_Authorization="Bearer wallpapers",
        )
        self.assertEqual(resp.status_code, 200)
