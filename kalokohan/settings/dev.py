from .base import *  # noqa

DJANGO_ENV = "development"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-nvg5arlsvczsdk5pzu-=f2qpst%ze8#jyuhfmldp7--j#ao5)j"  # pragma: allowlist secret  # nosec

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# wallpapers settings

WALLPAPERS_API_KEY = "wallpapers"  # pragma: allowlist secret
WALLPAPERS_UNSPLASH_CLIENT_CLASS = "kalokohan.wallpapers.clients.DummyUnsplashClient"
WALLPAPERS_LITTERBOX_CLIENT_CLASS = "kalokohan.wallpapers.clients.DummyLitterboxClient"
WALLPAPERS_UNSPLASH_ACCESS_ID = "unsplash_client_id"

# weather settings

WEATHER_OPEN_METEO_CLIENT_CLASS = "kalokohan.weather.clients.DummyOpenMeteoClient"
