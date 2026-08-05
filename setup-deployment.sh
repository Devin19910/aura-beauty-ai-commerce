#!/bin/bash

# AUTONOMOUS DEPLOYMENT SETUP
# This script handles: GitHub + Vercel deployment
# Run with: bash setup-deployment.sh YOUR-GITHUB-USERNAME

set -e

GITHUB_USERNAME=$1

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GitHub username required"
    echo "Usage: bash setup-deployment.sh YOUR-GITHUB-USERNAME"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════"
echo "🚀 AUTONOMOUS DEPLOYMENT SETUP"
echo "════════════════════════════════════════════════"
echo ""

# STEP 1: Verify we're in the right directory
echo "[1/4] Verifying project directory..."
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: Not in project root. Run from: aura-beauty-ai-commerce/"
    exit 1
fi
echo "✅ Project verified"
echo ""

# STEP 2: Check git status
echo "[2/4] Preparing git repository..."
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "⚠️  Remote 'origin' already exists. Removing..."
    git remote remove origin
fi

# Add GitHub remote
REPO_URL="https://github.com/${GITHUB_USERNAME}/aura-beauty-ai-commerce.git"
git remote add origin "$REPO_URL"
echo "✅ Added GitHub remote: $REPO_URL"
echo ""

# STEP 3: Prepare branches
echo "[3/4] Preparing git branches..."
if git rev-parse --verify main >/dev/null 2>&1; then
    echo "✅ Main branch exists"
else
    git branch -M main
    echo "✅ Created main branch"
fi

# Ensure we're on main
git checkout main
echo "✅ Switched to main branch"
echo ""

# STEP 4: Push to GitHub
echo "[4/4] Pushing to GitHub..."
echo ""
echo "⚠️  Important: You need to:"
echo "   1. Go to: https://github.com/new"
echo "   2. Create repository named: aura-beauty-ai-commerce"
echo "   3. Leave all settings as default"
echo "   4. Click 'Create repository'"
echo ""
echo "Then run:"
echo "   git push -u origin main"
echo ""
echo "After that, go to: https://vercel.com/new"
echo "Select 'Import from Git' and choose your repository"
echo ""

echo "════════════════════════════════════════════════"
echo "✅ SETUP COMPLETE!"
echo "════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "1. Create GitHub repo: https://github.com/new"
echo "2. Push code: git push -u origin main"
echo "3. Deploy: https://vercel.com/new → Import Git repo"
echo ""
