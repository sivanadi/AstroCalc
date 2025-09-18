#!/bin/bash
# User data script for EC2 instance deployment

set -e

# Variables passed from Terraform
PROJECT_NAME="${project_name}"
DOMAIN_NAME="${domain_name}"

echo "🚀 Setting up Vedic Astrology Calculator on $(date)"

# Update system
yum update -y

# Install Docker
yum install -y docker git
service docker start
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install Python and uv
yum install -y python3 python3-pip
pip3 install uv

# Create application directory
mkdir -p /opt/vedic-astrology
cd /opt/vedic-astrology

# Clone repository (replace with your actual repository)
git clone https://github.com/your-username/vedic-astrology-calculator.git .

# Build and start the application
docker-compose -f docker-compose.prod.yml up -d

# Install and configure nginx
yum install -y nginx
cp deployment/nginx/nginx.conf /etc/nginx/nginx.conf

# Generate SSL certificate (self-signed for initial setup)
mkdir -p /etc/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/key.pem \
    -out /etc/nginx/ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=${DOMAIN_NAME}"

# Start nginx
systemctl enable nginx
systemctl start nginx

# Install CloudWatch agent
yum install -y amazon-cloudwatch-agent

# Create CloudWatch config
cat << EOF > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
{
  "metrics": {
    "namespace": "VedicAstrology",
    "metrics_collected": {
      "cpu": {
        "measurement": ["cpu_usage_idle", "cpu_usage_iowait"],
        "metrics_collection_interval": 60
      },
      "disk": {
        "measurement": ["used_percent"],
        "metrics_collection_interval": 60,
        "resources": ["*"]
      },
      "mem": {
        "measurement": ["mem_used_percent"],
        "metrics_collection_interval": 60
      }
    }
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/nginx/access.log",
            "log_group_name": "/aws/ec2/vedic-astrology/nginx/access",
            "log_stream_name": "{instance_id}"
          },
          {
            "file_path": "/var/log/nginx/error.log",
            "log_group_name": "/aws/ec2/vedic-astrology/nginx/error",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
EOF

# Start CloudWatch agent
systemctl enable amazon-cloudwatch-agent
systemctl start amazon-cloudwatch-agent

echo "✅ Vedic Astrology Calculator deployment completed!"
echo "🌐 Application should be available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"