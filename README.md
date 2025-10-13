# Django Kubernetes Deployment

A production-ready Django application with Kubernetes deployment using GitLab CI/CD.

## Features
- 🐳 Docker containerization
- ☸️ Kubernetes deployment with Kustomize
- 🚀 GitLab CI/CD pipeline
- 🔄 Automatic database migrations
- 📧 Email & Slack notifications
- 🔒 Secure secret management

## Required GitLab CI/CD Variables

Set these in your GitLab project (Settings → CI/CD → Variables):

```bash
# GCP Configuration
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1
GCP_SERVICE_ACCOUNT_KEY=base64-encoded-service-account-key

# Kubernetes Configuration  
GKE_CLUSTER_NAME=your-cluster-name
GKE_ZONE=us-central1-a

# Database Configuration
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password

# Django Configuration
CI_SECRET_KEY=your-django-secret-key

# Notifications (Optional)
SENDGRID_API_KEY=your-sendgrid-key
SLACK_WEBHOOK_URL=your-slack-webhook
```

## Quick Start

1. **Setup development environment:**
   ```bash
   ./setup-dev.sh
   ```

2. **Configure your secrets:**
   ```bash
   # Edit with your real values
   vim k8s/overlays/prod/secrets.env
   ```

3. **Deploy:**
   ```bash
   git push origin main  # Triggers automatic deployment
   ```

## Architecture

```
├── k8s/                    # Kubernetes manifests
│   ├── base/              # Base configuration
│   └── overlays/          # Environment-specific configs
├── scripts/               # Automation scripts
└── .gitlab-ci.yml        # CI/CD pipeline
```
