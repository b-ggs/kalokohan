import os
from pathlib import Path

import dj_database_url
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DJANGO_ENV = os.getenv("DJANGO_ENV", "production")

SECRET_KEY = os.getenv("SECRET_KEY", "")

if allowed_hosts := os.getenv("ALLOWED_HOSTS"):
    ALLOWED_HOSTS = allowed_hosts.split(",")
else:
    ALLOWED_HOSTS = []

if csrf_trusted_origins := os.getenv("CSRF_TRUSTED_ORIGINS"):
    CSRF_TRUSTED_ORIGINS = csrf_trusted_origins.split(",")
else:
    CSRF_TRUSTED_ORIGINS = []


# Application definition

INSTALLED_APPS = [
    # Project apps
    "kalokohan.home",
    "kalokohan.utils",
    "kalokohan.users",
    # Third-party apps
    "django_extensions",
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # Simplified static file serving
    # https://devcenter.heroku.com/articles/django-assets
    # https://warehouse.python.org/project/whitenoise/
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "kalokohan.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "kalokohan", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "kalokohan.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if "DATABASE_URL" in os.environ:
    DATABASES = {
        "default": dj_database_url.parse(os.environ["DATABASE_URL"]),
    }


# Email
# https://docs.djangoproject.com/en/5.2/topics/email/

EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "25"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "false").lower() == "true"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "false").lower() == "true"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "kalokohan@localhost")


# Internationalization and localization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
# https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-LANGUAGE_CODE
# https://docs.djangoproject.com/en/5.2/ref/settings/#languages
# https://docs.djangoproject.com/en/5.2/ref/settings/#locale-paths

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("tl", _("Tagalog")),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, "kalokohan", "locale")]


# Use a custom User model
# https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = "users.User"


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATICFILES_DIRS = [
    # Static files such as images and other assets can be stored in
    # `kalokohan/static`
    os.path.join(BASE_DIR, "kalokohan", "static"),
    # Static files that are built by external tooling, e.g. Tailwind
    # are stored in `kalokohan/static_built`
    os.path.join(BASE_DIR, "kalokohan", "static_built"),
]

# Collected static files will be stored in static_collected
STATIC_ROOT = os.path.join(BASE_DIR, "static_collected")

# Static files will be served under /static/
STATIC_URL = "/static/"


# Simplified static file serving
# https://devcenter.heroku.com/articles/django-assets
# https://warehouse.python.org/project/whitenoise/

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
# https://docs.djangoproject.com/en/5.2/topics/logging/#configuring-logging

# Log everything from INFO above to stdout
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}][{process:d}][{levelname}][{name}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Error reporting
# https://docs.sentry.io/platforms/python/guides/django/
# https://glitchtip.com/sdkdocs/python-django

if sentry_dsn := os.getenv("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.utils import get_default_release

    SENTRY_ENVIRONMENT = DJANGO_ENV

    # Attempt to get release version from Sentry's utils and a couple other
    # environment variables
    def get_release_version():
        release = get_default_release()
        # Use GIT_REV for Dokku
        release = release or os.getenv("GIT_REV")
        # Use DJANGO_ENV as a final fallback
        return release or DJANGO_ENV

    sentry_init_args = {
        "dsn": sentry_dsn,
        "integrations": [DjangoIntegration()],
        "environment": SENTRY_ENVIRONMENT,
        "release": get_release_version(),
        "traces_sample_rate": 0.01,
    }

    # Auto session tracking is not supported by GlitchTip
    if "sentry.io" in sentry_dsn:
        sentry_init_args["auto_session_tracking"] = True
    else:
        sentry_init_args["auto_session_tracking"] = False

    sentry_sdk.init(**sentry_init_args)
