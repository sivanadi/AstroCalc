#!/bin/bash

# Oracle Cloud Infrastructure setup script for Vedic Astrology Calculator
set -e

echo "🚀 Setting up Vedic Astrology Calculator on Oracle Cloud..."

# Update system
echo "📦 Updating system packages..."
sudo yum update -y

# Install Docker
echo "🐳 Installing Docker..."
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install docker-compose
echo "🔧 Installing docker-compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/vedic-astrology
sudo chown $USER:$USER /opt/vedic-astrology
cd /opt/vedic-astrology

# Clone or copy application code (assumes code is already on the instance)
echo "📋 Application should be deployed to: /opt/vedic-astrology"

# Create docker-compose file
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  vedic-astrology:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ENVIRONMENT=production
      - DATA_DIR=/app/data
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - vedic-astrology
    restart: unless-stopped
EOF

# Create nginx configuration
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server vedic-astrology:8080;
    }

    server {
        listen 80;
        server_name _;

        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name _;

        # SSL configuration (add your certificates)
        # ssl_certificate /etc/nginx/ssl/cert.pem;
        # ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

# Create directories
mkdir -p data ssl

# Set firewall rules
echo "🔥 Configuring firewall..."
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload

echo "✅ Oracle Cloud setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Copy your application code to /opt/vedic-astrology"
echo "2. Add SSL certificates to the ssl/ directory"
echo "3. Run: docker-compose up -d"
echo "4. Configure your domain to point to this instance's public IP"
echo ""
echo "🌐 Your application will be available on:"
echo "   http://YOUR_PUBLIC_IP"
echo "   https://YOUR_PUBLIC_IP (after SSL setup)"