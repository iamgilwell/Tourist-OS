"""
Staging settings for Tourist Management System.
Use this for staging/pre-production environment testing.
"""

from .production import *

# Override some production settings for staging

# Slightly more relaxed security for testing
DEBUG = os.getenv("DEBUG", "False") == "True"

# Allowed hosts can be more permissive in staging
ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,staging.touristmanagement.com"
).split(",")

# Database - Separate staging database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "tourist_staging"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 300,  # Shorter connection pooling for staging
    }
}

# Email - Log emails to console in staging for testing
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# Or use a test email service like Mailtrap:
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.mailtrap.io"
# EMAIL_PORT = 2525

# Less strict security for staging (but still secure)
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False") == "True"
SECURE_HSTS_SECONDS = 0  # Disable HSTS in staging

# Cache - Can use Redis or local memory
CACHES = {
    "default": {
        "BACKEND": (
            "django.core.cache.backends.locmem.LocMemCache"
            if not os.getenv("REDIS_URL")
            else "django.core.cache.backends.redis.RedisCache"
        ),
        "LOCATION": os.getenv("REDIS_URL", "unique-staging-cache"),
    }
}

# Logging - More verbose in staging
LOGGING["root"]["level"] = "DEBUG"
LOGGING["loggers"]["django"]["level"] = "DEBUG"
LOGGING["loggers"]["django.request"]["level"] = "DEBUG"

# Add SQL query logging in staging
LOGGING["loggers"]["django.db.backends"] = {
    "handlers": ["console"],
    "level": os.getenv("SQL_DEBUG_LEVEL", "INFO"),
    "propagate": False,
}

# Staging-specific settings
STAGING_MODE = True

# Allow test payments (if using payment gateway)
PAYMENT_TEST_MODE = True

print("🧪 Staging settings loaded")
print(f"📊 Database: {DATABASES['default']['NAME']} at {DATABASES['default']['HOST']}")
print(f"🔒 Debug mode: {DEBUG}")
print(f"🌐 Allowed hosts: {ALLOWED_HOSTS}")
