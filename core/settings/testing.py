"""
Testing settings for Tourist Management System.
Use this for running automated tests (pytest, unittest, etc.)
"""

from .base import *

# SECURITY WARNING: Use a fixed test key
SECRET_KEY = "test-secret-key-not-for-production-use-only-in-tests"

# Debug should be False in tests to catch production-like issues
DEBUG = False

# Test hosts
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

# Database - Use in-memory SQLite for faster tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Alternatively, use PostgreSQL for more realistic tests:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "test_tourist_db",
#         "USER": "postgres",
#         "PASSWORD": "postgres",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

# Password hashers - Use faster hashers for testing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable password validators in tests
AUTH_PASSWORD_VALIDATORS = []

# Email - Use in-memory backend for tests
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Cache - Use dummy cache (no caching) in tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Static files - Disable collectstatic in tests
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Media files - Use temporary directory for test uploads
MEDIA_ROOT = os.path.join(BASE_DIR, "test_media")

# Logging - Minimal logging in tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "ERROR",  # Only show errors in tests
    },
}

# Disable migrations for faster tests (use --nomigrations flag)
# Or set MIGRATION_MODULES if you want to disable specific app migrations

# Testing-specific settings
TESTING_MODE = True

# Celery - Use eager mode for synchronous task execution in tests
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_TASK_EAGER_PROPAGATES = True

# Disable throttling in tests
# REST_FRAMEWORK = {
#     "DEFAULT_THROTTLE_CLASSES": [],
#     "DEFAULT_THROTTLE_RATES": {},
# }

print("🧪 Testing settings loaded - Using in-memory database")
