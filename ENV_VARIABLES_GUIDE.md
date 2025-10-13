# Environment Variables - Complete Guide

## 📋 Overview

Your Tourist Management System now has complete environment variable configuration for all deployment scenarios.

## 📁 Files Created

```
✅ .env.example          - Template with all available variables
✅ .env                  - Local development configuration (git-ignored)
✅ k8s/base/django/configmap.yaml - Production ConfigMap (updated)
✅ k8s/base/django/secret.yaml    - Production Secrets (updated)
```

## 🚀 Quick Setup

### Local Development

```bash
# 1. Copy example file
cp .env.example .env

# 2. Edit .env with your local settings (already configured for you!)
# No changes needed for basic local development

# 3. Run the application
python manage.py migrate
python manage.py runserver

# ✅ Application will use development settings automatically
```

### Production (Kubernetes)

Your K8s manifests have been updated with all necessary environment variables!

**Just update these critical values in production:**

1. **Generate new SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

2. **Update `k8s/base/django/secret.yaml`:**
```yaml
SECRET_KEY: "your-generated-secret-key-here"  # ← CHANGE THIS!
POSTGRES_PASSWORD: "your-secure-password"      # ← CHANGE THIS!
DEBUG: "False"                                 # ← Should be False
```

3. **Update `k8s/base/django/configmap.yaml`:**
```yaml
DJANGO_ALLOWED_HOSTS: "yourdomain.com,api.yourdomain.com"  # ← CHANGE THIS!
DEFAULT_FROM_EMAIL: "noreply@yourdomain.com"               # ← CHANGE THIS!
```

## 📊 Environment Variables Reference

### Core Django Settings

| Variable | Development | Production | Description |
|----------|------------|------------|-------------|
| `DJANGO_ENVIRONMENT` | `development` | `production` | Sets which settings file to use |
| `SECRET_KEY` | Auto-generated | **REQUIRED** | Django secret key (min 50 chars) |
| `DEBUG` | `True` | `False` | Enable/disable debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | **Your domains** | Comma-separated allowed hosts |

### Database Configuration

| Variable | Example | Description |
|----------|---------|-------------|
| `POSTGRES_DB` | `tourist_dev` | Database name |
| `POSTGRES_USER` | `postgres` | Database username |
| `POSTGRES_PASSWORD` | `postgres` | Database password |
| `POSTGRES_HOST` | `localhost` | Database host |
| `POSTGRES_PORT` | `5432` | Database port |

### Email Configuration

| Variable | Example | Description |
|----------|---------|-------------|
| `EMAIL_HOST` | `smtp.gmail.com` | SMTP server |
| `EMAIL_PORT` | `587` | SMTP port |
| `EMAIL_USE_TLS` | `True` | Use TLS encryption |
| `EMAIL_HOST_USER` | `your@email.com` | SMTP username |
| `EMAIL_HOST_PASSWORD` | `your-password` | SMTP password |
| `DEFAULT_FROM_EMAIL` | `noreply@domain.com` | Default sender email |
| `ADMIN_EMAIL` | `admin@domain.com` | Admin notification email |

### Security Settings (Production)

| Variable | Value | Description |
|----------|-------|-------------|
| `SECURE_SSL_REDIRECT` | `True` | Redirect HTTP to HTTPS |
| `SESSION_COOKIE_SECURE` | `True` | Secure session cookies |
| `CSRF_COOKIE_SECURE` | `True` | Secure CSRF cookies |

### Cache Configuration (Optional)

| Variable | Example | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://redis:6379/1` | Redis connection URL |

### Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `DEFAULT_COMMISSION_RATE` | `10.00` | Platform commission % |
| `DEFAULT_CURRENCY` | `USD` | Default currency code |
| `BOOKING_CANCELLATION_HOURS` | `24` | Min hours to cancel |
| `TIME_ZONE` | `UTC` | Application timezone |
| `LANGUAGE_CODE` | `en-us` | Default language |

## 🔐 Security Best Practices

### 1. SECRET_KEY

**❌ BAD:**
```yaml
SECRET_KEY: "django-insecure-short-key"
```

**✅ GOOD:**
```yaml
SECRET_KEY: "7k$m9p@2vn#x8q!r4w&e5t6y+u7i*o0p@a3s5d6f7g8h9j!k2l#z4x5c6v7b8n9m0"
```

Generate with:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 2. DEBUG Mode

**Production:** MUST be `False`
```yaml
DEBUG: "False"  # Production
```

**Development:** Can be `True`
```bash
DEBUG=True  # Development only
```

### 3. ALLOWED_HOSTS

**❌ BAD (Production):**
```yaml
DJANGO_ALLOWED_HOSTS: "*"  # Too permissive!
```

**✅ GOOD (Production):**
```yaml
DJANGO_ALLOWED_HOSTS: "touristmgmt.com,www.touristmgmt.com,api.touristmgmt.com"
```

### 4. Database Passwords

**❌ BAD:**
```yaml
POSTGRES_PASSWORD: "postgres"  # Default password
```

**✅ GOOD:**
```yaml
POSTGRES_PASSWORD: "Xk9@mP#4vN2$qR7!wE8"  # Strong password
```

## 📦 Complete .env File Template

```bash
# ==============================================================================
# ENVIRONMENT
# ==============================================================================
DJANGO_ENVIRONMENT=development

# ==============================================================================
# DJANGO CORE
# ==============================================================================
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# ==============================================================================
# DATABASE
# ==============================================================================
POSTGRES_DB=tourist_dev
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# ==============================================================================
# EMAIL
# ==============================================================================
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@touristmanagement.com
SERVER_EMAIL=server@touristmanagement.com
ADMIN_EMAIL=admin@touristmanagement.com

# ==============================================================================
# CACHE (Optional)
# ==============================================================================
REDIS_URL=redis://localhost:6379/1

# ==============================================================================
# SECURITY (Production)
# ==============================================================================
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# ==============================================================================
# APPLICATION SETTINGS
# ==============================================================================
DEFAULT_COMMISSION_RATE=10.00
DEFAULT_CURRENCY=USD
BOOKING_CANCELLATION_HOURS=24
TIME_ZONE=UTC
LANGUAGE_CODE=en-us
```

## 🔄 Environment Switching

### Local Development
```bash
export DJANGO_ENVIRONMENT=development
python manage.py runserver
# Uses settings from: core/settings/development.py
```

### Production
```yaml
# k8s/base/django/configmap.yaml
DJANGO_ENVIRONMENT: "production"
# Uses settings from: core/settings/production.py
```

### Staging
```yaml
DJANGO_ENVIRONMENT: "staging"
# Uses settings from: core/settings/staging.py
```

### Testing
```bash
export DJANGO_ENVIRONMENT=testing
python manage.py test
# Uses settings from: core/settings/testing.py
```

## ✅ Pre-Deployment Checklist

Before deploying to production, verify:

- [ ] Generated new `SECRET_KEY` (min 50 characters)
- [ ] Set `DEBUG=False`
- [ ] Updated `DJANGO_ALLOWED_HOSTS` with actual domains
- [ ] Changed `POSTGRES_PASSWORD` from default
- [ ] Configured email settings (SMTP)
- [ ] Set `DJANGO_ENVIRONMENT=production`
- [ ] Enabled security settings (SSL redirect, secure cookies)
- [ ] Reviewed all environment variables
- [ ] Tested locally first
- [ ] Verified K8s ConfigMap and Secret

## 🐛 Troubleshooting

### Environment not loading

**Check:**
```bash
python manage.py shell
```
```python
from django.conf import settings
print(getattr(settings, 'PRODUCTION_MODE', 'DEV'))
```

### Variables not being read

**Check K8s pod:**
```bash
kubectl exec -it <pod-name> -- env | grep DJANGO
```

### Email not working

**Test email configuration:**
```python
from django.core.mail import send_mail
send_mail('Test', 'Message', 'from@email.com', ['to@email.com'])
```

## 📚 Related Documentation

- **SETTINGS_GUIDE.md** - Complete settings documentation
- **ENV_SETUP_README.md** - Quick setup guide
- **TOURIST_SYSTEM_GUIDE.md** - System overview

## 🎯 Next Steps

1. ✅ Review your `.env` file
2. ✅ Update K8s secrets with production values
3. ✅ Generate new SECRET_KEY for production
4. ✅ Configure email provider
5. ✅ Deploy and verify!

---

**🎉 Environment configuration complete and production-ready!**
