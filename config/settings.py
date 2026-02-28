from pathlib import Path
import os
from dotenv import load_dotenv


# Base

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env ONLY if it exists (important for CI)
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Core settings

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-secret-key")

DEBUG = os.environ.get("DEBUG", "False") == "True"

# ALLOWED_HOSTS = ["*"]  # restrict later in production
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Applications

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # local apps
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


# Database (default: PostgreSQL)

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


# CI OVERRIDE (SQLite)

if os.getenv("CI", "").lower() == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "ci_test.sqlite3",
        }
    }


# Auth / Passwords

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
MEDIA_ROOT = "app/media"


# Security

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Behind nginx later
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Auth redirects

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/users/redirect/"
LOGOUT_REDIRECT_URL = "/login/"


# Security Hardening

# Prevent MIME sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# XSS filter
SECURE_BROWSER_XSS_FILTER = True  

# Clickjacking protection
X_FRAME_OPTIONS = "DENY"

# Referrer policy
SECURE_REFERRER_POLICY = "same-origin"

# Cookies (False for localhost HTTP)
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# If behind reverse proxy (nginx)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")