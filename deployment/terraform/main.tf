# Terraform configuration for Vedic Astrology Calculator
# Multi-cloud deployment with AWS, GCP, and Azure support

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Variables
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "vedic-astrology"
}

variable "cloud_provider" {
  description = "Cloud provider (aws, gcp, azure)"
  type        = string
  default     = "aws"
  validation {
    condition     = contains(["aws", "gcp", "azure"], var.cloud_provider)
    error_message = "Cloud provider must be aws, gcp, or azure."
  }
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = "vedic-astrology.your-domain.com"
}

variable "instance_type" {
  description = "Instance type"
  type        = string
  default     = "t3.medium"  # AWS
}

variable "region" {
  description = "Cloud region"
  type        = string
  default     = "us-west-2"  # Default for AWS
}

# Local values
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
    Application = "vedic-astrology-calculator"
  }
}

# Data sources
data "aws_ami" "amazon_linux" {
  count       = var.cloud_provider == "aws" ? 1 : 0
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# AWS Resources
resource "aws_vpc" "main" {
  count                = var.cloud_provider == "aws" ? 1 : 0
  cidr_block          = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-vpc"
  })
}

resource "aws_subnet" "public" {
  count                   = var.cloud_provider == "aws" ? 1 : 0
  vpc_id                  = aws_vpc.main[0].id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = data.aws_availability_zones.available[0].names[0]
  map_public_ip_on_launch = true
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-public-subnet"
  })
}

data "aws_availability_zones" "available" {
  count = var.cloud_provider == "aws" ? 1 : 0
  state = "available"
}

resource "aws_internet_gateway" "main" {
  count  = var.cloud_provider == "aws" ? 1 : 0
  vpc_id = aws_vpc.main[0].id
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-igw"
  })
}

resource "aws_route_table" "public" {
  count  = var.cloud_provider == "aws" ? 1 : 0
  vpc_id = aws_vpc.main[0].id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main[0].id
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-public-rt"
  })
}

resource "aws_route_table_association" "public" {
  count          = var.cloud_provider == "aws" ? 1 : 0
  subnet_id      = aws_subnet.public[0].id
  route_table_id = aws_route_table.public[0].id
}

resource "aws_security_group" "web" {
  count       = var.cloud_provider == "aws" ? 1 : 0
  name        = "${var.project_name}-web-sg"
  description = "Security group for web server"
  vpc_id      = aws_vpc.main[0].id
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH"
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP"
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound"
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-web-sg"
  })
}

# User data script
locals {
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    project_name = var.project_name
    domain_name  = var.domain_name
  }))
}

resource "aws_instance" "web" {
  count                  = var.cloud_provider == "aws" ? 1 : 0
  ami                    = data.aws_ami.amazon_linux[0].id
  instance_type          = var.instance_type
  key_name              = aws_key_pair.main[0].key_name
  vpc_security_group_ids = [aws_security_group.web[0].id]
  subnet_id             = aws_subnet.public[0].id
  user_data             = local.user_data
  
  root_block_device {
    volume_type = "gp3"
    volume_size = 20
    encrypted   = true
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-web-server"
  })
}

resource "aws_key_pair" "main" {
  count      = var.cloud_provider == "aws" ? 1 : 0
  key_name   = "${var.project_name}-key"
  public_key = file("~/.ssh/id_rsa.pub")  # Assumes you have SSH key
  
  tags = local.common_tags
}

resource "aws_eip" "web" {
  count      = var.cloud_provider == "aws" ? 1 : 0
  instance   = aws_instance.web[0].id
  domain     = "vpc"
  depends_on = [aws_internet_gateway.main[0]]
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-eip"
  })
}

# S3 bucket for backups
resource "aws_s3_bucket" "backups" {
  count  = var.cloud_provider == "aws" ? 1 : 0
  bucket = "${var.project_name}-backups-${random_id.bucket_suffix[0].hex}"
  
  tags = local.common_tags
}

resource "aws_s3_bucket_versioning" "backups" {
  count  = var.cloud_provider == "aws" ? 1 : 0
  bucket = aws_s3_bucket.backups[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "backups" {
  count  = var.cloud_provider == "aws" ? 1 : 0
  bucket = aws_s3_bucket.backups[0].id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "random_id" "bucket_suffix" {
  count       = var.cloud_provider == "aws" ? 1 : 0
  byte_length = 4
}

# CloudWatch monitoring
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  count               = var.cloud_provider == "aws" ? 1 : 0
  alarm_name          = "${var.project_name}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  
  dimensions = {
    InstanceId = aws_instance.web[0].id
  }
  
  tags = local.common_tags
}

# Outputs
output "public_ip" {
  description = "Public IP of the web server"
  value       = var.cloud_provider == "aws" ? aws_eip.web[0].public_ip : ""
}

output "website_url" {
  description = "URL of the deployed application"
  value       = var.cloud_provider == "aws" ? "http://${aws_eip.web[0].public_ip}" : ""
}

output "ssh_command" {
  description = "SSH command to connect to the server"
  value       = var.cloud_provider == "aws" ? "ssh -i ${aws_key_pair.main[0].key_name}.pem ec2-user@${aws_eip.web[0].public_ip}" : ""
}