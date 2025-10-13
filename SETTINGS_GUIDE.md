# Settings Configuration Guide

## 📁 Settings Structure

Your project now uses environment-based settings for better configuration management:

```
core/
├── settings/
│   ├── __init__.py        # Auto-loads correct environment
│   ├── base.py            # Common settings for all environments
│   ├── development.py     # Local development settings
│   ├── staging.py         # Pre-production/staging settings
│   ├── production.py      # Production settings (K8s, GCP)
│   └── testing.py         # Test/CI settings
└── settings.py.old        # Backup of old settings (can be deleted)
```

## 🚀 Usage

### Setting the Environment

Set the `DJANGO_ENVIRONMENT` environment variable to choose which settings to use:

```bash
# Development (default if not set)
export DJANGO_ENVIRONMENT=development
python manage.py runserver

# Staging
export DJANGO_ENVIRONMENT=staging
python manage.py runserver

# Production
export DJANGO_ENVIRONMENT=production
gunicorn core.wsgi:application

# Testing
export DJANGO_ENVIRONMENT=testing
python manage.py test
```

### In Docker/Kubernetes

Update your deployment configurations:

**Dockerfile:**
```dockerfile
# Set default environment
ENV DJANGO_ENVIRONMENT=production
```

**K8s ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: django-config
data:
  DJANGO_ENVIRONMENT: "production"
  # ... other configs
```

## 📝 Environment Details

### 1. Development Settings (`development.py`)

**When to use:** Local development on your machine

**Features:**
- ✅ Debug mode enabled
- ✅ Relaxed security settings
- ✅ Console email backend (emails print to console)
- ✅ SQLite or local PostgreSQL
- ✅ Verbose logging with SQL queries
- ✅ No password validators (easier testing)
- ✅ Local memory cache

**Environment Variables:**
```bash
DJANGO_ENVIRONMENT=development
SECRET_KEY=optional  # Uses fallback if not set
POSTGRES_DB=tourist_dev
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

**Run Commands:**
```bash
export DJANGO_ENVIRONMENT=development
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
```

### 2. Production Settings (`production.py`)

**When to use:** Production deployment (K8s, GCP, AWS, etc.)

**Features:**
- ✅ Debug mode disabled
- ✅ Strict security settings (HTTPS, HSTS, secure cookies)
- ✅ SMTP email backend
- ✅ PostgreSQL with connection pooling
- ✅ Redis cache
- ✅ WhiteNoise for static files
- ✅ JSON logging for better monitoring
- ✅ Error reporting to admins

**Required Environment Variables:**
```bash
DJANGO_ENVIRONMENT=production
SECRET_KEY=your-super-secret-key-here  # REQUIRED!
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com  # REQUIRED!
POSTGRES_DB=tourist_production
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com

# Cache (optional but recommended)
REDIS_URL=redis://redis-host:6379/1

# Security (optional, defaults shown)
SECURE_SSL_REDIRECT=True
DEBUG=False
```

**K8s Secret Example:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: django-secret
type: Opaque
stringData:
  SECRET_KEY: "your-super-secret-production-key-min-50-chars-long"
  POSTGRES_PASSWORD: "your-secure-db-password"
  EMAIL_HOST_PASSWORD: "your-email-password"
```

### 3. Staging Settings (`staging.py`)

**When to use:** Pre-production testing environment

**Features:**
- ✅ Based on production settings
- ✅ Slightly relaxed security for testing
- ✅ Console email backend (or test service like Mailtrap)
- ✅ Separate staging database
- ✅ More verbose logging than production
- ✅ SQL query logging available

**Environment Variables:**
```bash
DJANGO_ENVIRONMENT=staging
SECRET_KEY=staging-secret-key
DJANGO_ALLOWED_HOSTS=staging.yourdomain.com
POSTGRES_DB=tourist_staging
POSTGRES_USER=staging_user
POSTGRES_PASSWORD=staging_password
POSTGRES_HOST=staging-db-host
DEBUG=False  # or True for debugging

# Optional
SQL_DEBUG_LEVEL=DEBUG  # To see SQL queries
```

### 4. Testing Settings (`testing.py`)

**When to use:** Running automated tests (pytest, unittest, CI/CD)

**Features:**
- ✅ In-memory SQLite database (fast tests)
- ✅ Dummy cache (no caching)
- ✅ In-memory email backend
- ✅ Faster password hashers
- ✅ No password validators
- ✅ Minimal logging
- ✅ Debug disabled

**Usage:**
```bash
# Run tests
export DJANGO_ENVIRONMENT=testing
python manage.py test

# Or in GitLab CI
script:
  - export DJANGO_ENVIRONMENT=testing
  - python manage.py test
```

## 🔒 Security Checklist for Production

Before deploying to production, ensure:

- [ ] `SECRET_KEY` is set and unique (min 50 characters)
- [ ] `DEBUG=False` in production
- [ ] `DJANGO_ALLOWED_HOSTS` is properly configured
- [ ] Database credentials are in secrets (not hardcoded)
- [ ] Email configuration is set up
- [ ] Redis is configured for caching
- [ ] HTTPS is enabled (`SECURE_SSL_REDIRECT=True`)
- [ ] Static files are collected (`python manage.py collectstatic`)
- [ ] Migrations are run (`python manage.py migrate`)

## 🔧 Common Tasks

### Generate Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or in bash:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Check Current Settings

```python
# In Django shell
python manage.py shell

from django.conf import settings
print(f"Environment: {getattr(settings, 'PRODUCTION_MODE', 'Development')}")
print(f"Debug: {settings.DEBUG}")
print(f"Database: {settings.DATABASES['default']['NAME']}")
print(f"Allowed Hosts: {settings.ALLOWED_HOSTS}")
```

### Update GitLab CI

Update `.gitlab-ci.yml` to use production settings:

```yaml
deploy-to-k8s:
  stage: deploy
  variables:
    DJANGO_ENVIRONMENT: production
  script:
    # Your deployment scripts
```

## 📊 Settings Comparison

| Feature | Development | Staging | Production | Testing |
|---------|------------|---------|------------|---------|
| **DEBUG** | ✅ True | ⚠️ Optional | ❌ False | ❌ False |
| **Database** | SQLite/Local PG | Staging PG | Production PG | SQLite (memory) |
| **Cache** | Local Memory | Redis/Memory | Redis | Dummy |
| **Email** | Console | Console/Test | SMTP | Memory |
| **Security** | Relaxed | Medium | Strict | Minimal |
| **Logging** | Verbose | Verbose | Structured | Minimal |
| **Static Files** | Dev Server | WhiteNoise | WhiteNoise | Static |

## 🐛 Troubleshooting

### Issue: Settings import error

**Error:** `ModuleNotFoundError: No module named 'core.settings.development'`

**Solution:**
- Check that `DJANGO_ENVIRONMENT` is set correctly
- Verify all settings files exist in `core/settings/`
- Ensure `__init__.py` exists in the settings folder

### Issue: SECRET_KEY error in production

**Error:** `ValueError: SECRET_KEY environment variable must be set in production!`

**Solution:**
```bash
# Set in K8s secret
kubectl create secret generic django-secret \
  --from-literal=SECRET_KEY='your-secret-key-here'

# Or set environment variable
export SECRET_KEY='your-secret-key-here'
```

### Issue: ALLOWED_HOSTS error

**Error:** `CommandError: You must set DJANGO_ALLOWED_HOSTS`

**Solution:**
```bash
# In K8s ConfigMap
DJANGO_ALLOWED_HOSTS: "yourdomain.com,www.yourdomain.com,api.yourdomain.com"

# Or as environment variable
export DJANGO_ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
```

## 📚 Additional Resources

### Recommended Production Setup

1. **Database:** PostgreSQL with connection pooling
2. **Cache:** Redis for sessions and cache
3. **Static Files:** WhiteNoise or Cloud Storage (GCS, S3)
4. **Media Files:** Cloud Storage (GCS, S3)
5. **Email:** SMTP service (SendGrid, Mailgun, AWS SES)
6. **Monitoring:** Sentry for error tracking
7. **Logging:** Structured JSON logs

### Environment Variables Reference

Create a `.env.example` file for your team:

```bash
# .env.example
DJANGO_ENVIRONMENT=development
SECRET_KEY=generate-your-own-secret-key
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=tourist_dev
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Email (optional in dev)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Cache (optional)
REDIS_URL=redis://localhost:6379/1
```

## ✅ Migration from Old Settings

Your old `settings.py` has been backed up to `settings.py.old`.

**No changes needed to:**
- ✅ `manage.py` - Already uses `core.settings`
- ✅ `wsgi.py` - Already uses `core.settings`
- ✅ Existing code - Everything works the same

**To verify migration:**
```bash
# Run this and check for environment message
python manage.py check

# Should see: "🔧 Development settings loaded" (or your environment)
```

---

**🎉 You now have a professional, environment-based settings structure!**
