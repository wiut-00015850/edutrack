from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "build.sqlite3",
    }
}

STATIC_ROOT = "/app/staticfiles"