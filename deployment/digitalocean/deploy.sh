#!/bin/bash

# Digital Ocean App Platform deployment script for Vedic Astrology Calculator
set -e

echo "🚀 Starting Digital Ocean App Platform deployment..."

# Configuration
APP_NAME=${1:-"vedic-astrology-calculator"}
REPO_URL=${2:-""}

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "❌ doctl CLI not found. Installing..."
    
    # Detect OS and install doctl
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -sL https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-linux-amd64.tar.gz | tar -xzv
        sudo mv doctl /usr/local/bin
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install doctl
    else
        echo "Please install doctl manually: https://docs.digitalocean.com/reference/doctl/how-to/install/"
        exit 1
    fi
fi

# Check authentication
if ! doctl account get &> /dev/null; then
    echo "❌ Digital Ocean authentication required. Please run:"
    echo "   doctl auth init"
    exit 1
fi

# Check if repository URL is provided
if [ -z "$REPO_URL" ]; then
    echo "❌ Please provide your GitHub repository URL:"
    echo "   ./deploy.sh app-name https://github.com/username/repo"
    exit 1
fi

echo "📋 Application: $APP_NAME"
echo "📂 Repository: $REPO_URL"

# Update app.yaml with repository URL
sed -i.bak "s|your-username/vedic-astrology-calculator|${REPO_URL#https://github.com/}|g" deployment/digitalocean/app.yaml

# Create the app
echo "🏗️ Creating Digital Ocean App..."
CREATE_OUTPUT=$(doctl apps create deployment/digitalocean/app.yaml --format ID --no-header 2>&1)

# Extract app ID from output
if [[ $CREATE_OUTPUT =~ [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12} ]]; then
    APP_ID="${BASH_REMATCH[0]}"
    echo "✅ App created with ID: $APP_ID"
else
    echo "❌ Failed to create app. Output: $CREATE_OUTPUT"
    exit 1
fi

echo "⏳ Waiting for deployment to complete..."
doctl apps get $APP_ID --wait

# Get app URL
APP_URL=$(doctl apps get $APP_ID --format "DefaultIngress" --no-header)

echo "✅ Deployment completed successfully!"
echo "🌐 Your Vedic Astrology Calculator is available at:"
echo "   https://$APP_URL"
echo ""
echo "📊 To view logs:"
echo "   doctl apps logs $APP_ID"
echo ""
echo "💰 Estimated monthly cost: $5-12 USD"
echo "   (basic-xxs instance)"
echo ""
echo "🔧 To update your app:"
echo "   doctl apps update $APP_ID --spec=deployment/digitalocean/app.yaml"

# Restore original app.yaml
mv deployment/digitalocean/app.yaml.bak deployment/digitalocean/app.yaml