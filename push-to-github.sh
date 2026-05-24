#!/bin/bash
# One-command push script for GitHub Pages deployment
# Run this from the repo directory

REPO_NAME="leadgenmini"

echo "🚀 LeadGenMini — Push to GitHub Pages"
echo "=========================================="

# Check if gh is logged in
if ! gh auth status > /dev/null 2>&1; then
    echo "❌ GitHub CLI not authenticated."
    echo "   Please run: gh auth login"
    echo "   Then run this script again."
    exit 1
fi

echo "✅ GitHub CLI authenticated"

# Get GitHub username
USERNAME=$(gh api user --jq '.login')
if [ -z "$USERNAME" ]; then
    echo "❌ Could not get GitHub username"
    exit 1
fi
echo "👤 GitHub user: $USERNAME"

# Create the remote repo (public, no template)
echo "📦 Creating repo $REPO_NAME..."
gh repo create "$REPO_NAME" --public --description "LeadGenMini — Targeted lead lists in minutes" --confirm

# Add remote and push
git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git" 2>/dev/null || true
git branch -M main
git push -u origin main

echo ""
echo "✅ Code pushed to: https://github.com/$USERNAME/$REPO_NAME"
echo ""
echo "🔧 NEXT: Enable GitHub Pages:"
echo "   1. Visit: https://github.com/$USERNAME/$REPO_NAME/settings/pages"
echo "   2. Under 'Branch' select 'main'"
echo "   3. Under 'Folder' select '/ (root)'"
echo "   4. Click Save"
echo ""
echo "🌐 Your site will be at: https://$USERNAME.github.io/$REPO_NAME"
echo "   (takes ~2 minutes to go live)"
