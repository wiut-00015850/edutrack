from pathlib import Path
import os
from dotenv import load_dotenv


# Base directory

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables (.env optional)

env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Core settings

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-secret-key")

# DEBUG is defined in dev.py or prod.py
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


# Applications

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "users.apps.UsersConfig",
    "courses",
    "assignments",
]


# Middleware

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# URLs / Templates

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database (PostgreSQL default)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "edutrack"),
        "USER": os.getenv("DB_USER", "edutrack_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "edutrack_password"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# CI override (SQLite)
if os.getenv("CI", "").lower() == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "ci_test.sqlite3",
        }
    }


# Auth / Password Validation

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static & Media

STATIC_URL = "/static/"
STATIC_ROOT = "/app/staticfiles/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/app/media/"


# Default Primary Key

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Security (base defaults - production overrides in prod.py)

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "http")
CSRF_TRUSTED_ORIGINS = (os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if
os.getenv("CSRF_TRUSTED_ORIGINS")
    else []
)

USE_X_FORWARDED_HOST = True

# Authentication Redirects

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/users/redirect/"
LOGOUT_REDIRECT_URL = "/login/"

# 

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
