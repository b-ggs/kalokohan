import factory
from faker import Faker

from kalokohan.utils.factories import BaseMetaFactory

from .types import UnsplashPhoto

fake = Faker()


class UnsplashPhotoFactory(
    factory.BaseDictFactory,
    metaclass=BaseMetaFactory[UnsplashPhoto],
):
    image_url = factory.LazyAttribute(
        lambda obj: f"https://via.placeholder.com/{fake.random_int(max=500)}x{fake.random_int(max=500)}.jpg"  # noqa: E501
    )
    item_url = factory.Faker("url")

    class Meta:
        model = UnsplashPhoto
