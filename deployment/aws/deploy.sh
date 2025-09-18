#!/bin/bash

# AWS Elastic Beanstalk deployment script for Vedic Astrology Calculator
set -e

echo "🚀 Starting AWS Elastic Beanstalk deployment..."

# Configuration
APP_NAME=${1:-"vedic-astrology-calculator"}
ENV_NAME="${APP_NAME}-prod"
REGION=${2:-"us-east-1"}

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install AWS CLI first:"
    echo "   https://aws.amazon.com/cli/"
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "❌ EB CLI not found. Installing..."
    pip install awsebcli
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run:"
    echo "   aws configure"
    exit 1
fi

echo "📋 Application: $APP_NAME"
echo "🌍 Environment: $ENV_NAME"
echo "🌎 Region: $REGION"

# Copy deployment files to root
cp deployment/aws/application.py .
cp deployment/aws/requirements.txt .
cp deployment/aws/Procfile .
cp -r deployment/aws/.ebextensions .

# Initialize EB application if not exists
if [ ! -f .elasticbeanstalk/config.yml ]; then
    echo "🔧 Initializing Elastic Beanstalk application..."
    eb init $APP_NAME --platform "Python 3.11" --region $REGION
fi

# Create environment and deploy
echo "🏗️ Creating environment and deploying..."
if eb list | grep -q $ENV_NAME; then
    echo "📦 Deploying to existing environment..."
    eb deploy $ENV_NAME
else
    echo "🆕 Creating new environment and deploying..."
    eb create $ENV_NAME --instance-type t3.micro --envvars ENVIRONMENT=production,DATA_DIR=/var/app/current/data
fi

# Get the application URL
APP_URL=$(eb status $ENV_NAME | grep "CNAME:" | awk '{print $2}')

echo "✅ Deployment completed successfully!"
echo "🌐 Your Vedic Astrology Calculator is available at:"
echo "   http://$APP_URL"
echo ""
echo "📊 To view logs:"
echo "   eb logs $ENV_NAME"
echo ""
echo "💰 Estimated monthly cost: $10-25 USD"
echo "   (t3.micro instance + data transfer)"
echo ""
echo "🧹 Cleanup deployment files..."
rm -f application.py requirements.txt Procfile
rm -rf .ebextensions