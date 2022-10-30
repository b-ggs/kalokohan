from .base import *  # noqa

DJANGO_ENV = "test"

SECRET_KEY = "test"  # pragma: allowlist secret  # nosec

# wallpapers settings

WALLPAPERS_UNSPLASH_CLIENT_CLASS = "kalokohan.wallpapers.clients.DummyUnsplashClient"
WALLPAPERS_LITTERBOX_CLIENT = "kalokohan.wallpapers.clients.DummyLitterboxClient"

WALLPAPERS_UNSPLASH_ACCESS_ID = "unsplash_client_id"
