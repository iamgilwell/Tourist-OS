# Environment Setup - Quick Reference

## ✅ What Has Been Created

Your Django project now has **professional environment-based settings**:

```
✅ core/settings/__init__.py       - Auto-loads environment
✅ core/settings/base.py           - Common settings
✅ core/settings/development.py    - Local development
✅ core/settings/staging.py        - Pre-production
✅ core/settings/production.py     - Production (K8s/GCP)
✅ core/settings/testing.py        - Testing/CI
```

## 🚀 Quick Start Guide

### Local Development

```bash
# 1. Set environment (optional, defaults to development)
export DJANGO_ENVIRONMENT=development

# 2. Run migrations
python manage.py migrate

# 3. Create superuser
python manage.py createsuperuser

# 4. Run development server
python manage.py runserver

# ✅ You should see: "🔧 Development settings loaded"
```

### Production (K8s/GCP)

**1. Update K8s ConfigMap:**
```yaml
# k8s/base/django/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: django-config
data:
  DJANGO_ENVIRONMENT: "production"  # ← ADD THIS
  POSTGRES_HOST: "0.0.0.0"
  POSTGRES_PORT: "YOUR PORT"
  DJANGO_ALLOWED_HOSTS: "*"
```

**2. Update K8s Secret:**
```yaml
# k8s/base/django/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: django-secret
type: Opaque
stringData:
  POSTGRES_DB: your-db
  POSTGRES_USER: your-username
  POSTGRES_PASSWORD: your-postgres-password
  SECRET_KEY: "generate-a-long-random-secret-key-min-50-chars"  # ← CHANGE THIS
  DEBUG: "False"  # ← CHANGE TO False in production
```

**3. Generate Production Secret Key:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**4. Deploy:**
```bash
# Your GitLab CI/CD will handle this, or manually:
kubectl apply -f k8s/base/django/
```

## 📝 Environment Variables by Environment

### Development (Default)
```bash
DJANGO_ENVIRONMENT=development
# All other variables optional, uses sensible defaults
```

### Production
```bash
DJANGO_ENVIRONMENT=production
SECRET_KEY=your-secret-key-here              # REQUIRED!
DJANGO_ALLOWED_HOSTS=domain1.com,domain2.com # REQUIRED!
POSTGRES_DB=tourist_production
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=your_db_host
POSTGRES_PORT=5432
DEBUG=False

# Email (recommended)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com

# Cache (optional but recommended)
REDIS_URL=redis://redis:6379/1
```

### Staging
```bash
DJANGO_ENVIRONMENT=staging
SECRET_KEY=staging-secret-key
DJANGO_ALLOWED_HOSTS=staging.yourdomain.com
POSTGRES_DB=tourist_staging
POSTGRES_USER=staging_user
POSTGRES_PASSWORD=staging_password
POSTGRES_HOST=staging-db
DEBUG=False
```

### Testing (CI/CD)
```bash
DJANGO_ENVIRONMENT=testing
# All other variables auto-configured for tests
```

## 🔍 Verify Your Setup

### Check Which Environment is Active

```bash
python manage.py shell
```

```python
from django.conf import settings

# Check environment
if hasattr(settings, 'PRODUCTION_MODE'):
    print("Running in PRODUCTION")
elif hasattr(settings, 'STAGING_MODE'):
    print("Running in STAGING")
elif hasattr(settings, 'TESTING_MODE'):
    print("Running in TESTING")
else:
    print("Running in DEVELOPMENT")

# Check other settings
print(f"Debug: {settings.DEBUG}")
print(f"Database: {settings.DATABASES['default']['NAME']}")
print(f"Allowed Hosts: {settings.ALLOWED_HOSTS}")
```

### Run Django Check

```bash
# Development check
python manage.py check

# Production check (shows security warnings)
python manage.py check --deploy
```

## 🚨 Important Production Checklist

Before deploying to production:

- [ ] Generate and set unique `SECRET_KEY` (min 50 characters)
- [ ] Set `DEBUG=False`
- [ ] Configure `DJANGO_ALLOWED_HOSTS` with your actual domains
- [ ] Set strong database password
- [ ] Configure email settings
- [ ] Set up Redis for caching (recommended)
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py migrate`
- [ ] Test that `DJANGO_ENVIRONMENT=production` is set

## 📦 Updated Dependencies

New production dependencies added to `requirements.txt`:

```
whitenoise>=6.5.0           # Static file serving
django-redis>=5.3.0         # Redis cache backend
redis>=5.0.0                # Redis client
python-json-logger>=2.0.7   # JSON logging
```

Install with:
```bash
pip install -r requirements.txt
```

## 🔄 Migration from Old Settings

Your old `core/settings.py` has been renamed to `core/settings.py.old` (backup).

**No code changes needed!** The new settings package is drop-in compatible.

If you want to delete the backup:
```bash
rm core/settings.py.old
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'core.settings.development'"

**Fix:** Ensure all settings files exist in `core/settings/` directory.

### "ValueError: SECRET_KEY environment variable must be set in production!"

**Fix:** Set SECRET_KEY in your K8s secret or environment:
```bash
export SECRET_KEY="your-secret-key-here"
```

### "CommandError: You must set DJANGO_ALLOWED_HOSTS"

**Fix:** Set in K8s ConfigMap or environment:
```bash
export DJANGO_ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
```

### Still using old settings?

**Check:**
```bash
ls -la core/settings/
```

Should show:
```
__init__.py
base.py
development.py
production.py
staging.py
testing.py
```

## 📚 Documentation

- **Full Settings Guide:** See `SETTINGS_GUIDE.md`
- **Tourist System Guide:** See `TOURIST_SYSTEM_GUIDE.md`

## 🎯 Next Steps

1. ✅ Test locally with development settings
2. ✅ Update your K8s manifests with production environment variables
3. ✅ Generate production SECRET_KEY
4. ✅ Deploy and verify production settings work
5. ✅ Set up monitoring and logging

## ✨ Benefits of New Settings Structure

- ✅ **Clear separation** between environments
- ✅ **Security** - Production requires proper configuration
- ✅ **Flexibility** - Easy to add new environments
- ✅ **Best practices** - Industry-standard Django setup
- ✅ **Team-friendly** - Easy for others to understand
- ✅ **CI/CD ready** - Works with GitLab, GitHub Actions, etc.

---

**🎉 Your Django project now has professional, production-ready settings!**

For questions, check:
1. `SETTINGS_GUIDE.md` - Detailed settings documentation
2. `TOURIST_SYSTEM_GUIDE.md` - Tourist management system guide
3. Django docs: https://docs.djangoproject.com/en/5.2/topics/settings/
