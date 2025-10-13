#!/bin/bash
set -e

echo "🔍 Checking secrets security..."

# Check if .gitignore exists
if [ ! -f ".gitignore" ]; then
    echo "❌ .gitignore file not found!"
    exit 1
fi

# Required gitignore patterns
REQUIRED_PATTERNS=(
    "k8s/overlays/*/secrets.env"
    "*.env"
    "__pycache__/"
)

# Check each required pattern
for pattern in "${REQUIRED_PATTERNS[@]}"; do
    if ! grep -q "$pattern" .gitignore; then
        echo "❌ Missing pattern in .gitignore: $pattern"
        echo "🔧 Adding $pattern to .gitignore..."
        echo "$pattern" >> .gitignore
    fi
done

# Check if any secrets.env files are staged for commit
if git diff --cached --name-only | grep -q "secrets\.env"; then
    echo "❌ ERROR: secrets.env files are staged for commit!"
    echo "🚨 This could expose sensitive information!"
    echo "📝 Files found:"
    git diff --cached --name-only | grep "secrets\.env"
    echo ""
    echo "🔧 To fix this, run:"
    echo "   git reset HEAD k8s/overlays/*/secrets.env"
    exit 1
fi

# Check if any .env files exist in the working directory that aren't ignored
if find . -name "*.env" -not -path "./.git/*" | grep -q .; then
    echo "⚠️  Found .env files in repository:"
    find . -name "*.env" -not -path "./.git/*"
    echo ""
    echo "🔍 Checking if they're properly ignored..."
    
    # Check if these files would be ignored by git
    for env_file in $(find . -name "*.env" -not -path "./.git/*"); do
        if git check-ignore "$env_file" >/dev/null 2>&1; then
            echo "✅ $env_file is properly ignored"
        else
            echo "❌ $env_file is NOT ignored and could be committed!"
            echo "🔧 Add this pattern to .gitignore: $(basename "$env_file")"
        fi
    done
fi

echo "✅ Secrets security check passed!"
