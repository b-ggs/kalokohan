import json

import responses
from django.test import TestCase, override_settings

from kalokohan.wallpapers.clients import get_litterbox_client, get_unsplash_client


@override_settings(
    WALLPAPERS_UNSPLASH_CLIENT_CLASS="kalokohan.wallpapers.clients.UnsplashClient",
    WALLPAPERS_UNSPLASH_ACCESS_ID="unsplash_access_id",
)
class UnsplashClientTest(TestCase):
    def setUp(self) -> None:
        self.base_url = "http://api.unsplash.fake"
        self.unsplash_client = get_unsplash_client(
            base_url=self.base_url,
        )

    @responses.activate
    def test_get_random_photo(self) -> None:
        with open("kalokohan/wallpapers/fixtures/photos_random_resp.json") as file:
            raw = file.read()

        fake_response = json.loads(raw)

        responses.add(
            responses.GET,
            f"{self.base_url}/photos/random",
            headers={
                "Accept-Version": "v1",
                "Authorization": "Client-ID unsplash_access_id",
            },
            json=fake_response,
        )

        random_photo = self.unsplash_client.get_random_photo()

        self.assertEqual(random_photo.image_url, fake_response["urls"]["full"])
        self.assertEqual(random_photo.item_url, fake_response["links"]["html"])


@override_settings(
    WALLPAPERS_LITTERBOX_CLIENT="kalokohan.wallpapers.clients.LitterboxClient",
)
class LitterboxClientTest(TestCase):
    def setUp(self) -> None:
        self.base_url = "http://litterbox.fake"
        self.unsplash_client = get_litterbox_client(
            base_url=self.base_url,
        )

    @responses.activate
    def test_upload_image(self) -> None:
        image_binary = b"fake_image_binary"
        fake_response = "https://litterbox.fake/abcd.jpg"

        files = {
            "reqtype": (None, "fileupload"),
            "time": (None, "1h"),
            "fileToUpload": ("image.jpg", image_binary),
        }

        responses.add(
            responses.POST,
            self.base_url,
            match=[responses.matchers.multipart_matcher(files)],
            body=fake_response.encode(),
        )

        upload_photo_resp = self.unsplash_client.upload_image(image_binary=image_binary)

        self.assertEqual(upload_photo_resp, fake_response)
