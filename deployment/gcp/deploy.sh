#!/bin/bash

# Google Cloud Platform deployment script for Vedic Astrology Calculator
set -e

echo "🚀 Starting Google Cloud deployment..."

# Configuration
PROJECT_ID=${1:-"your-project-id"}
SERVICE_NAME="vedic-astrology-calculator"
REGION="us-central1"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install Google Cloud SDK first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if project is set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo "❌ Please provide your Google Cloud project ID:"
    echo "   ./deploy.sh YOUR_PROJECT_ID"
    exit 1
fi

echo "📋 Using project: $PROJECT_ID"
echo "🌍 Region: $REGION"

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy using Cloud Build
echo "🏗️ Building and deploying with Cloud Build..."
gcloud builds submit --config=deployment/gcp/cloudbuild.yaml .

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform=managed --region=$REGION --format='value(status.url)')

echo "✅ Deployment completed successfully!"
echo "🌐 Your Vedic Astrology Calculator is available at:"
echo "   $SERVICE_URL"
echo ""
echo "📊 To view logs:"
echo "   gcloud logs read --resource=cloud_run_revision --service=$SERVICE_NAME"
echo ""
echo "💰 Estimated monthly cost for light usage: $0-5 USD"
echo "   (Free tier includes 2M requests/month)"