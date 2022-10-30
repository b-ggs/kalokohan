from typing import Literal, NamedTuple


class UnsplashPhoto(NamedTuple):
    # Direct link to the image
    image_url: str
    # Link to the photo page on Unsplash
    item_url: str


PhotoOrientations = Literal[
    "landscape",
    "portrait",
    "squarish",
]
