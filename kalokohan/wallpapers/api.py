import logging
from typing import TypedDict

import requests
from django.http import HttpRequest
from ninja import Router

from kalokohan.wallpapers.models import PastRandomPhoto

from .clients import get_litterbox_client, get_unsplash_client
from .security import AuthBearer

router = Router()

logger = logging.getLogger(__name__)


class GetWallpaperResponse(TypedDict):
    image_url: str
    item_url: str
    litterbox_url: str


@router.get("/", auth=AuthBearer())
def get_wallpaper(
    request: HttpRequest,
    query: str = "",
) -> GetWallpaperResponse:
    """
    Get a random photo from Unsplash, download the image, upload the image to
    Litterbox, and return the Unsplash and Litterbox URLs.
    """

    client = get_unsplash_client()
    unsplash_photo = client.get_random_photo(
        query=query,
    )

    # Store photo but if something goes wrong, just log the exception and
    # continue
    try:
        PastRandomPhoto.objects.create(
            image_url=unsplash_photo.image_url,
            item_url=unsplash_photo.item_url,
        )
    except Exception as e:
        logger.exception(e)

    resp = requests.get(unsplash_photo.image_url)
    image_binary = resp.content

    client = get_litterbox_client()
    litterbox_url = client.upload_image(image_binary)

    return GetWallpaperResponse(
        image_url=unsplash_photo.image_url,
        item_url=unsplash_photo.item_url,
        litterbox_url=litterbox_url,
    )
