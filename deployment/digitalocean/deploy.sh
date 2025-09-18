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
CREATE_OUTPUT=$(doctl apps create --spec deployment/digitalocean/app.yaml --output json 2>/dev/null)

if [ $? -eq 0 ]; then
    APP_ID=$(echo "$CREATE_OUTPUT" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
    echo "✅ App created with ID: $APP_ID"
else
    echo "❌ Failed to create app. Please check your configuration and doctl authentication."
    # Restore original app.yaml
    if [ -f deployment/digitalocean/app.yaml.bak ]; then
        mv deployment/digitalocean/app.yaml.bak deployment/digitalocean/app.yaml
    fi
    exit 1
fi

echo "⏳ Waiting for deployment to complete..."
# Wait for the app to be deployed (polling approach since --wait isn't available on apps get)
for i in {1..60}; do
    STATUS=$(doctl apps get $APP_ID --output json | python3 -c "import sys, json; print(json.load(sys.stdin)['active_deployment']['phase'])" 2>/dev/null)
    if [ "$STATUS" = "ACTIVE" ]; then
        echo "✅ Deployment completed successfully!"
        break
    elif [ "$STATUS" = "ERROR" ] || [ "$STATUS" = "CANCELED" ]; then
        echo "❌ Deployment failed with status: $STATUS"
        exit 1
    else
        echo "   Status: $STATUS... (attempt $i/60)"
        sleep 10
    fi
done

if [ "$STATUS" != "ACTIVE" ]; then
    echo "❌ Deployment timed out after 10 minutes"
    exit 1
fi

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