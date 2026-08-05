#!/usr/bin/env powershell

# AUTONOMOUS DEPLOYMENT SETUP
# This script handles: GitHub + Vercel deployment
# Run with: .\setup-deployment.ps1 -GitHubUsername YOUR-GITHUB-USERNAME

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername
)

Write-Host ""
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🚀 AUTONOMOUS DEPLOYMENT SETUP" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# STEP 1: Verify project directory
Write-Host "[1/4] Verifying project directory..." -ForegroundColor Yellow
if (-not (Test-Path "vercel.json")) {
    Write-Host "❌ Error: Not in project root" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Project verified" -ForegroundColor Green
Write-Host ""

# STEP 2: Check git repository
Write-Host "[2/4] Preparing git repository..." -ForegroundColor Yellow
try {
    git rev-parse --git-dir | Out-Null
}
catch {
    Write-Host "❌ Error: Not a git repository" -ForegroundColor Red
    exit 1
}

# Remove existing remote if it exists
try {
    git remote get-url origin | Out-Null
    Write-Host "⚠️  Remote 'origin' exists. Removing..." -ForegroundColor Yellow
    git remote remove origin
}
catch {
    # Remote doesn't exist, continue
}

# Add GitHub remote
$repoUrl = "https://github.com/${GitHubUsername}/aura-beauty-ai-commerce.git"
git remote add origin $repoUrl
Write-Host "✅ Added GitHub remote: $repoUrl" -ForegroundColor Green
Write-Host ""

# STEP 3: Prepare branches
Write-Host "[3/4] Preparing git branches..." -ForegroundColor Yellow
try {
    git rev-parse --verify main | Out-Null
    Write-Host "✅ Main branch exists" -ForegroundColor Green
}
catch {
    git branch -M main
    Write-Host "✅ Created main branch" -ForegroundColor Green
}

# Ensure we're on main
git checkout main | Out-Null
Write-Host "✅ Switched to main branch" -ForegroundColor Green
Write-Host ""

# STEP 4: Show next steps
Write-Host "[4/4] Ready to push to GitHub" -ForegroundColor Yellow
Write-Host ""

Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣  CREATE GITHUB REPOSITORY" -ForegroundColor Cyan
Write-Host "   → Go to: https://github.com/new" -ForegroundColor White
Write-Host "   → Repository name: aura-beauty-ai-commerce" -ForegroundColor White
Write-Host "   → Click 'Create repository'" -ForegroundColor White
Write-Host ""

Write-Host "2️⃣  PUSH CODE TO GITHUB" -ForegroundColor Cyan
Write-Host "   → Run: git push -u origin main" -ForegroundColor White
Write-Host ""

Write-Host "3️⃣  DEPLOY TO VERCEL" -ForegroundColor Cyan
Write-Host "   → Go to: https://vercel.com/new" -ForegroundColor White
Write-Host "   → Click 'Import from Git'" -ForegroundColor White
Write-Host "   → Select: aura-beauty-ai-commerce" -ForegroundColor White
Write-Host "   → Click 'Deploy'" -ForegroundColor White
Write-Host ""

Write-Host "That's it! Your website will be live in 60 seconds! 🚀" -ForegroundColor Green
Write-Host ""

# Display git status
Write-Host "Current git status:" -ForegroundColor Yellow
git log --oneline -3
