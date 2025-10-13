"""
Development settings for Tourist Management System.
Use this for local development.
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-dev-key-change-this-in-production-!@#$%^&*()"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "192.168.49.2", "*"]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "tourist_dev"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Debug Toolbar (Optional - uncomment if you want to use it)
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
# INTERNAL_IPS = ["127.0.0.1"]

# Email - Console backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable password validators in development for easier testing
AUTH_PASSWORD_VALIDATORS = []

# CORS Settings for local development (if using separate frontend)
# INSTALLED_APPS += ["corsheaders"]
# MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE
# CORS_ALLOW_ALL_ORIGINS = True

# Cache - Simple local memory cache for development
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Static files - Simplified for development
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Logging - More verbose in development
LOGGING["root"]["level"] = "DEBUG"
LOGGING["loggers"]["django"]["level"] = "DEBUG"

# Development-specific settings
DEVELOPMENT_MODE = True

# Show SQL queries in console (helpful for debugging)
LOGGING["loggers"]["django.db.backends"] = {
    "handlers": ["console"],
    "level": "DEBUG",
    "propagate": False,
}

print("🔧 Development settings loaded")
print(f"📊 Database: {DATABASES['default']['NAME']} at {DATABASES['default']['HOST']}")
