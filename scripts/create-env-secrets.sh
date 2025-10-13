#!/bin/bash
set -e

echo "🔧 Checking environment secrets..."

# Define environments
ENVS=("dev" "staging" "prod")

# Template for secrets.env
create_secrets_template() {
    local env=$1
    local debug_value="True"
    local password_suffix="dev123"
    
    if [ "$env" = "prod" ]; then
        debug_value="False"
        password_suffix="CHANGE_ME_IN_PRODUCTION"
    elif [ "$env" = "staging" ]; then
        debug_value="False"
        password_suffix="staging456"
    fi

    cat > "k8s/overlays/$env/secrets.env" << EOF
POSTGRES_DB=tourist_os
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password_$password_suffix
SECRET_KEY=django-$env-secret-key-$(date +%s)
DEBUG=$debug_value
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EOF
}

# Create missing environment directories and secrets
for env in "${ENVS[@]}"; do
    ENV_DIR="k8s/overlays/$env"
    SECRETS_FILE="$ENV_DIR/secrets.env"
    
    # Create directory if it doesn't exist
    if [ ! -d "$ENV_DIR" ]; then
        echo "📁 Creating $ENV_DIR directory..."
        mkdir -p "$ENV_DIR"
    fi
    
    # Create secrets.env if it doesn't exist
    if [ ! -f "$SECRETS_FILE" ]; then
        echo "🔐 Creating $SECRETS_FILE..."
        create_secrets_template "$env"
        echo "✅ Created $SECRETS_FILE with template values"
    else
        echo "✅ $SECRETS_FILE already exists"
    fi
    
    # Create kustomization.yaml if it doesn't exist
    KUSTOMIZATION_FILE="$ENV_DIR/kustomization.yaml"
    if [ ! -f "$KUSTOMIZATION_FILE" ]; then
        echo "📝 Creating $KUSTOMIZATION_FILE..."
        cat > "$KUSTOMIZATION_FILE" << EOF
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

secretGenerator:
- name: django-secret
  behavior: replace
  envs:
  - secrets.env
EOF
        
        # Add replica patch for dev environment
        if [ "$env" = "dev" ]; then
            echo "" >> "$KUSTOMIZATION_FILE"
            echo "patches:" >> "$KUSTOMIZATION_FILE"
            echo "- patch: |-" >> "$KUSTOMIZATION_FILE"
            echo "    - op: replace" >> "$KUSTOMIZATION_FILE"
            echo "      path: /spec/replicas" >> "$KUSTOMIZATION_FILE"
            echo "      value: 1" >> "$KUSTOMIZATION_FILE"
            echo "  target:" >> "$KUSTOMIZATION_FILE"
            echo "    kind: Deployment" >> "$KUSTOMIZATION_FILE"
            echo "    name: django-deployment" >> "$KUSTOMIZATION_FILE"
        fi
        
        echo "✅ Created $KUSTOMIZATION_FILE"
    fi
done

echo "🎉 All environment secrets are ready!"
