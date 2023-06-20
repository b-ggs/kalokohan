import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from faker import Faker
from pydantic.utils import import_string

from .factories import UnsplashPhotoFactory
from .types import PhotoOrientations, UnsplashPhoto

fake = Faker()


class BaseUnsplashClient:
    def __init__(self, base_url: str = "") -> None:
        self.base_url = base_url

    def get_random_photo(
        self,
        query: str = "",
        orientation: PhotoOrientations | None = None,
    ) -> UnsplashPhoto:
        """
        Returns a random photo from Unsplash

        https://unsplash.com/documentation#get-a-random-photo
        """

        raise NotImplementedError()


class DummyUnsplashClient(BaseUnsplashClient):
    def get_random_photo(
        self,
        query: str = "",
        orientation: PhotoOrientations | None = None,
    ) -> UnsplashPhoto:
        """
        Returns a random photo from Unsplash

        https://unsplash.com/documentation#get-a-random-photo
        """

        return UnsplashPhotoFactory()


class UnsplashClient(BaseUnsplashClient):
    def __init__(self, base_url: str = "https://api.unsplash.com") -> None:
        super().__init__(base_url)

    def get_random_photo(
        self,
        query: str = "",
        orientation: PhotoOrientations | None = None,
    ) -> UnsplashPhoto:
        """
        Returns a random photo from Unsplash

        https://unsplash.com/documentation#get-a-random-photo
        """
        url = f"{self.base_url}/photos/random"

        params = {}
        if query:
            params["query"] = query
        if orientation:
            params["orientation"] = orientation

        resp = requests.get(
            url,
            params=params,
            headers=self.get_headers(),
            timeout=30,
        )

        if not resp.ok:
            resp.raise_for_status()

        resp_json = resp.json()

        return UnsplashPhoto(
            image_url=resp_json["urls"]["full"],
            item_url=resp_json["links"]["html"],
        )

    def get_headers(self) -> dict:
        if hasattr(settings, "WALLPAPERS_UNSPLASH_ACCESS_ID") and (
            access_id := settings.WALLPAPERS_UNSPLASH_ACCESS_ID
        ):
            return {
                "Accept-Version": "v1",
                "Authorization": f"Client-ID {access_id}",
            }

        raise ImproperlyConfigured("WALLPAPERS_UNSPLASH_ACCESS_ID is unset or blank")


def get_unsplash_client(**kwargs) -> BaseUnsplashClient:
    client_class = import_string(settings.WALLPAPERS_UNSPLASH_CLIENT_CLASS)
    return client_class(**kwargs)


class BaseLitterboxClient:
    def __init__(self, base_url: str = "") -> None:
        self.base_url = base_url

    def upload_image(self, image_binary: bytes) -> str:
        """
        Uploads an image to Litterbox and returns the resulting URL

        https://litterbox.catbox.moe/tools.php
        """

        raise NotImplementedError()


class DummyLitterboxClient(BaseLitterboxClient):
    def __init__(self, base_url: str = "") -> None:
        super().__init__(base_url)
        if not self.base_url:
            self.base_url = "http://litterbox.fake"

    def upload_image(self, image_binary: bytes) -> str:
        """
        Uploads an image to Litterbox and returns the resulting URL

        https://litterbox.catbox.moe/tools.php
        """

        return f"{self.base_url}/{fake.pystr()}.jpg"


class LitterboxClient(BaseLitterboxClient):
    def __init__(
        self,
        base_url: str = "https://litterbox.catbox.moe/resources/internals/api.php",
    ) -> None:
        super().__init__(base_url)

    def upload_image(self, image_binary: bytes) -> str:
        """
        Uploads an image to Litterbox and returns the resulting URL

        https://litterbox.catbox.moe/tools.php
        """

        resp = requests.post(
            self.base_url,
            files={
                "reqtype": (None, "fileupload"),
                "time": (None, "1h"),
                "fileToUpload": ("image.jpg", image_binary),
            },
            timeout=30,
        )

        if not resp.ok:
            resp.raise_for_status()

        return resp.content.decode("utf-8").strip()


def get_litterbox_client(**kwargs) -> BaseLitterboxClient:
    client_class = import_string(settings.WALLPAPERS_LITTERBOX_CLIENT)
    return client_class(**kwargs)
