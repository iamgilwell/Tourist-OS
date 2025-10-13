#!/bin/bash
echo "🚀 Setting up development environment..."

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial setup
echo "🔧 Running initial environment setup..."
./scripts/create-env-secrets.sh

echo "✅ Development environment ready!"
echo ""
echo "📝 Next steps:"
echo "1. Edit k8s/overlays/*/secrets.env with your real values"
echo "2. Never commit secrets.env files (they're in .gitignore)"
echo "3. Pre-commit will run automatically on each commit"
