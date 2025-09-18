# Cloud Deployment Guide for Vedic Astrology Calculator

This directory contains deployment configurations and scripts for deploying the Vedic Astrology Calculator to major cloud platforms.

## Quick Start

### Universal Installer (Recommended)
```bash
# Show cloud deployment options
python install.py cloud

# Deploy to specific platform
python install.py cloud gcp
python install.py cloud aws
python install.py cloud oracle  
python install.py cloud digitalocean
```

### Manual Deployment
Each platform has its own deployment script:
```bash
# Google Cloud Run
./deployment/gcp/deploy.sh YOUR_PROJECT_ID

# AWS Elastic Beanstalk
./deployment/aws/deploy.sh app-name us-east-1

# Oracle Cloud
./deployment/oracle/compute_setup.sh

# Digital Ocean
./deployment/digitalocean/deploy.sh app-name https://github.com/user/repo
```

## Platform Comparison

| Platform | Cost | Setup Time | Best For | Free Tier |
|----------|------|------------|----------|-----------|
| **Google Cloud Run** | $0-5/month | 5 min | Serverless, auto-scaling | 2M requests/month |
| **AWS Elastic Beanstalk** | $10-25/month | 15 min | Enterprise, full AWS ecosystem | 750 hours/month |
| **Oracle Cloud** | $0-10/month | 20 min | Cost-effective, always-free tier | Always free compute |
| **Digital Ocean** | $5-12/month | 10 min | Developer-friendly, simple | $200 credit (60 days) |

## Platform-Specific Guides

### Google Cloud Run
- **Serverless**: Scales to zero when not in use
- **Pay-per-use**: Only pay for actual requests
- **Automatic HTTPS**: SSL certificates handled automatically
- **Global**: Deployed to multiple regions automatically

Files:
- `gcp/Dockerfile` - Container configuration
- `gcp/cloudbuild.yaml` - Build and deployment pipeline
- `gcp/deploy.sh` - Automated deployment script

### AWS Elastic Beanstalk
- **Full AWS Integration**: Access to RDS, CloudWatch, etc.
- **Auto Scaling**: Handles traffic spikes automatically
- **Load Balancer**: Built-in application load balancer
- **Health Monitoring**: Comprehensive health checks

Files:
- `aws/application.py` - WSGI entry point
- `aws/.ebextensions/01_python.config` - Environment configuration
- `aws/requirements.txt` - Python dependencies
- `aws/deploy.sh` - Automated deployment script

### Oracle Cloud Infrastructure
- **Always Free Tier**: Generous free resources
- **High Performance**: Excellent price/performance ratio
- **Manual Setup**: More control over infrastructure
- **Docker Support**: Containerized deployment

Files:
- `oracle/Dockerfile` - Container configuration
- `oracle/compute_setup.sh` - Instance setup script

### Digital Ocean App Platform
- **GitHub Integration**: Deploy directly from repository
- **Simple Scaling**: Easy vertical and horizontal scaling
- **Managed Database**: Optional managed PostgreSQL
- **Developer Experience**: Streamlined deployment process

Files:
- `digitalocean/app.yaml` - App platform specification
- `digitalocean/deploy.sh` - Automated deployment script

## Environment Variables

All platforms support these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment type | `production` |
| `DATA_DIR` | Database directory | `/app/data` |
| `PORT` | Server port | `8080` |

### Security Variables (Optional)
| Variable | Description |
|----------|-------------|
| `ADMIN_USERNAME` | Admin panel username |
| `ADMIN_PASSWORD_HASH` | Bcrypt hash of admin password |
| `SESSION_TIMEOUT` | Session timeout in seconds |
| `CORS_ORIGINS` | Allowed CORS origins |

## Database Considerations

### SQLite (Default)
- **File-based**: Database stored in container filesystem
- **Limitations**: Single instance only, data lost on container restart
- **Best for**: Development, low-traffic applications

### Managed Database (Recommended for Production)
For production deployments, consider using managed database services:

- **Google Cloud SQL** (PostgreSQL)
- **AWS RDS** (PostgreSQL)
- **Oracle Autonomous Database**
- **Digital Ocean Managed Database**

To use PostgreSQL instead of SQLite, update your environment variables:
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

## SSL/HTTPS

All platforms provide automatic HTTPS:
- **Google Cloud Run**: Automatic SSL certificates
- **AWS Elastic Beanstalk**: ALB with SSL termination
- **Oracle Cloud**: Manual SSL certificate setup
- **Digital Ocean**: Automatic SSL certificates

## Monitoring and Logs

### Google Cloud Run
```bash
gcloud logs read --resource=cloud_run_revision --service=vedic-astrology-calculator
```

### AWS Elastic Beanstalk
```bash
eb logs production
```

### Oracle Cloud
```bash
docker logs <container-name>
```

### Digital Ocean
```bash
doctl apps logs <app-id>
```

## Scaling

| Platform | Scaling Type | Configuration |
|----------|--------------|---------------|
| Google Cloud Run | Automatic | Concurrent requests, memory limits |
| AWS Elastic Beanstalk | Auto/Manual | Instance count, CPU/memory thresholds |
| Oracle Cloud | Manual | Container replicas, load balancer |
| Digital Ocean | Vertical | Instance size upgrade |

## Cost Optimization

### Free Tier Usage
1. **Google Cloud**: 2M requests/month free
2. **AWS**: 750 hours t2.micro free (1 year)
3. **Oracle**: Always free tier (2 OCPUs, 24GB RAM)
4. **Digital Ocean**: $200 credit for new accounts

### Production Cost Estimates
- **Light usage** (< 10k requests/month): $0-10/month
- **Medium usage** (100k requests/month): $5-30/month  
- **High usage** (1M requests/month): $20-100/month

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Ensure Python 3.11+ is specified
   - Check requirements.txt is present
   - Verify ephemeris files are included

2. **Runtime Errors**
   - Check environment variables
   - Verify port configuration (8080 for cloud, 5000 for local)
   - Ensure data directory permissions

3. **Database Issues**
   - SQLite permissions in container
   - PostgreSQL connection string format
   - Database migration on deployment

### Debug Commands

```bash
# Check deployment logs
python install.py cloud [platform] --debug

# Test API endpoint
curl https://your-app-url.com/health

# Check database connection
curl https://your-app-url.com/admin
```

## Support

For deployment issues:
1. Check platform-specific documentation
2. Review deployment logs
3. Verify environment configuration
4. Test locally before deploying

Each platform directory contains additional README files with detailed setup instructions.