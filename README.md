# Vedic Astrology Calculator API

A comprehensive FastAPI web application for Vedic astrology calculations using Swiss Ephemeris. Features secure admin panel with rate limiting, 40+ ayanamsha systems, multiple house systems, and professional astronomical calculations with both natal and transit chart support.

## Features

### Core Astrology Engine
- **40+ Ayanamsha Systems**: J.N. Bhasin (default), Krishnamurti (fallback), Lahiri, Raman, Yukteshwar, and many more traditional and modern systems
- **9 Vedic Planets**: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu (North Node), Ketu (South Node)
- **Multiple House Systems**: Equal House (default), Topocentric (fallback), Placidus, and Sripati
- **Dual Chart Support**: Both natal and transit calculations in a single API call
- **High Precision**: Full 6-decimal precision with DMS (Degrees, Minutes, Seconds) format display
- **Swiss Ephemeris**: Professional-grade astronomical calculations with industry-standard accuracy
- **Timezone Support**: Comprehensive timezone handling with automatic UTC conversion

### User Interface
- **Responsive Frontend**: Modern HTML5/CSS3/JavaScript interface optimized for all devices
- **Enhanced Input Forms**: Combined date format (DD/MM/YYYY), time format (HH:MM:SS), timezone selection, and location coordinates
- **Real-time Results**: Instant chart calculations with copy-to-clipboard functionality
- **Professional Display**: Both simplified (2 decimal) and full precision (6 decimal) planetary positions
- **DMS Format**: Traditional Degrees°Minutes'Seconds" display for ayanamsha values

### Security & Access Control
- **API Key Authentication**: Generate and manage API keys with custom rate limiting
- **Domain Authorization**: Control which domains can access your API endpoints
- **Rate Limiting**: Configurable per-minute, daily, and monthly usage limits
- **Secure Admin Panel**: bcrypt password hashing with session-based authentication
- **Security Headers**: HSTS, CSP, XSS protection, and other modern security standards
- **Usage Tracking**: Comprehensive database-driven usage monitoring

### Advanced Admin Features
- **Rate Limit Management**: Set custom per-minute, daily, and monthly limits for each API key and domain
- **Enhanced Admin Panel**: Modern web interface with real-time rate limit display
- **Bulk Operations**: Manage multiple API keys and domains simultaneously
- **Advanced Filtering**: Pagination, search, sorting, and date-based filtering
- **Session Management**: Secure admin sessions with configurable timeouts
- **Password Management**: Secure password changes with strength validation

## Quick Start

### 1. Access the Application
The server runs automatically on port 5000. Open your browser and navigate to the frontend interface for easy chart calculations.

### 2. Admin Setup (First Time)
1. Go to `/admin` to access the admin login page
2. **IMPORTANT**: Set secure admin credentials via environment variables before first use
3. Default fallback credentials (if no env vars set): `admin` / `admin123`
4. **CRITICAL**: Configure proper environment variables for production deployment
5. Set up API keys with custom rate limits and authorized domains as needed

### 3. Frontend Interface
- Fill in birth details using combined formats: date (DD/MM/YYYY), time (HH:MM:SS), location coordinates
- Select your preferred timezone from the dropdown
- Choose from 40+ ayanamsha systems (default: J.N. Bhasin, fallback: Krishnamurti)
- Select house system (default: Equal House, fallback: Topocentric, also: Placidus, Sripati)
- Click "Calculate Chart" for instant natal and transit results
- Use copy buttons to copy specific planetary positions or full JSON

## API Documentation

### Authentication
API endpoints require either:
- **API Key Authentication**: Include `Authorization: Bearer <your_api_key>` header
- **Domain Authorization**: Access from pre-authorized domains (configure via admin panel)

**Rate Limiting**: Each API key and domain has configurable limits:
- **Per-minute limits**: Prevent burst abuse
- **Daily limits**: Control daily usage quotas
- **Monthly limits**: Manage subscription-style access

**API Key Usage Examples:**
```bash
# Using curl with API key
curl -H "Authorization: Bearer your_api_key_here" \
     "http://localhost:5000/chart?year=2024&month=9&day=16&hour=12&minute=30&second=15&lat=28.6139&lon=77.2090&tz=Asia/Kolkata"

# Using JavaScript fetch with API key
fetch('/chart', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your_api_key_here',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(chartData)
})
```

### Chart Calculation Endpoints

#### GET /chart
Calculate chart with URL parameters for external integrations.

**Parameters:**
- `year` (int): Year (e.g., 2024)
- `month` (int): Month (1-12)  
- `day` (int): Day (1-31)
- `hour` (int): Hour (0-23)
- `minute` (int): Minute (0-59) 
- `second` (int): Second (0-59)
- `lat` (float): Latitude in degrees (positive for North)
- `lon` (float): Longitude in degrees (positive for East)
- `tz` (string): Timezone (e.g., "Asia/Kolkata", "America/New_York")
- `ayanamsha` (string): Ayanamsha system (default: "jn_bhasin")
- `house_system` (string): House system (default: "equal")
- `natal_ayanamsha` (string): Natal chart ayanamsha (optional, falls back to ayanamsha)
- `natal_house_system` (string): Natal chart house system (optional, falls back to house_system)
- `transit_ayanamsha` (string): Transit chart ayanamsha (optional, falls back to ayanamsha)
- `transit_house_system` (string): Transit chart house system (optional, falls back to house_system)

**Example:**
```bash
# Basic chart calculation
curl -H "Authorization: Bearer your_api_key_here" \
     "http://localhost:5000/chart?year=2024&month=9&day=16&hour=12&minute=30&second=15&lat=28.6139&lon=77.2090&tz=Asia/Kolkata&ayanamsha=jn_bhasin&house_system=equal"

# Natal and transit with different systems
curl -H "Authorization: Bearer your_api_key_here" \
     "http://localhost:5000/chart?year=2024&month=9&day=16&hour=12&lat=28.6139&lon=77.2090&natal_ayanamsha=jn_bhasin&transit_ayanamsha=krishnamurti&natal_house_system=equal&transit_house_system=topocentric"
```

#### POST /chart
Calculate chart with JSON payload for programmatic access.

**Request Body:**
```json
{
  "year": 2024,
  "month": 9,
  "day": 16,
  "hour": 12,
  "minute": 30,
  "second": 15,
  "lat": 28.6139,
  "lon": 77.2090,
  "tz": "Asia/Kolkata",
  "ayanamsha": "jn_bhasin",
  "house_system": "equal",
  "natal_ayanamsha": "jn_bhasin",
  "natal_house_system": "equal",
  "transit_ayanamsha": "krishnamurti",
  "transit_house_system": "equal"
}
```

**Enhanced Response:**
```json
{
  "natal_chart": {
    "julian_day_ut": 2460569.79184,
    "ascendant_deg": 231.9,
    "ascendant_full_precision": 231.898513,
    "planets_deg": {
      "Sun": 149.8,
      "Moon": 304.26,
      "Mars": 72.65,
      "Mercury": 137.37,
      "Jupiter": 56.37,
      "Venus": 177.58,
      "Saturn": 321.31,
      "Rahu": 343.04,
      "Ketu": 163.04
    },
    "planets_full_precision": {
      "Sun": 149.803946,
      "Moon": 304.258996,
      "Mars": 72.654122,
      "Mercury": 137.372063,
      "Jupiter": 56.368941,
      "Venus": 177.582879,
      "Saturn": 321.305487,
      "Rahu": 343.042511,
      "Ketu": 163.042511
    },
    "ayanamsha_name": "N.C. Lahiri",
    "ayanamsha_value_decimal": 24.105409,
    "ayanamsha_value_dms": "24°06'19.47\"",
    "house_system_name": "Placidus"
  },
  "transit_chart": {
    "julian_day_ut": 2460569.79184,
    "ascendant_deg": 229.15,
    "ascendant_full_precision": 229.152847,
    "planets_deg": {
      "Sun": 147.92,
      "Moon": 302.41,
      "Mars": 70.78,
      "Mercury": 135.51,
      "Jupiter": 54.52,
      "Venus": 175.73,
      "Saturn": 319.46,
      "Rahu": 341.19,
      "Ketu": 161.19
    },
    "ayanamsha_name": "Krishnamurti",
    "ayanamsha_value_decimal": 23.987542,
    "house_system_name": "Equal House"
  },
  "timezone_used": "Asia/Kolkata",
  "input_time_ut": 7.004167
}
```

### Information Endpoints

#### GET /ayanamsha-options
List all 40+ available ayanamsha systems with their full names.

**Response:**
```json
{
  "lahiri": "N.C. Lahiri",
  "krishnamurti": "Krishnamurti",
  "raman": "B.V. Raman",
  "yukteshwar": "Yukteshwar",
  "true_citra": "True Citra",
  "true_revati": "True Revati",
  // ... 35+ more systems
}
```

#### GET /security-status
Security configuration status and system information.

#### GET /health  
Health check endpoint for monitoring and load balancers.

### Admin Endpoints (Protected)

#### Basic Admin Operations
- `GET /admin` - Admin login page
- `POST /admin/login` - Admin authentication  
- `POST /admin/logout` - Logout from current session
- `POST /admin/logout-all` - Emergency logout from all sessions
- `POST /admin/password-change` - Change admin password with validation

#### API Key Management
- `GET /admin/api-keys` - View API keys with current rate limits
- `POST /admin/api-keys` - Generate new API key with custom rate limits
- `PUT /admin/api-keys/{api_key_hash}/limits` - Update rate limits for existing API key
- `DELETE /admin/api-keys/{api_key_hash}` - Delete API key

#### Domain Management
- `GET /admin/domains` - View authorized domains with current rate limits
- `POST /admin/domains` - Add authorized domain with custom rate limits
- `PUT /admin/domains/{domain}/limits` - Update rate limits for existing domain
- `DELETE /admin/domains/{domain}` - Remove domain authorization

#### Enhanced V1 Admin API
- `GET /admin/v1/api-keys` - Enhanced API key retrieval with pagination, search, filtering, and sorting
- `POST /admin/v1/api-keys` - Create API key with enhanced validation
- `POST /admin/v1/api-keys/bulk` - Bulk operations on multiple API keys
- `GET /admin/v1/domains` - Enhanced domain retrieval with advanced filtering
- `POST /admin/v1/domains` - Create domain with enhanced validation
- `POST /admin/v1/domains/bulk` - Bulk operations on multiple domains

## Admin Configuration

### Rate Limit Management
The admin panel allows you to set custom rate limits for each API key and domain:

**API Key Rate Limits** (defaults):
- Per-minute: 60 requests
- Daily: 1,000 requests  
- Monthly: 30,000 requests

**Domain Rate Limits** (defaults):
- Per-minute: 10 requests
- Daily: 100 requests
- Monthly: 3,000 requests

**Admin Panel Features:**
1. **Create with Custom Limits**: Set specific rate limits when creating new API keys or domains
2. **Visual Display**: Current rate limits are clearly shown for all existing entries
3. **Real-time Updates**: Changes take effect immediately
4. **Usage Tracking**: Database tracks actual usage against limits automatically

### Security Setup
For production deployment, configure these environment variables:

```bash
# Admin Authentication (REQUIRED for production)
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD_HASH=your_bcrypt_hashed_password
# Optional fallback (NOT recommended for production):
# ADMIN_PASSWORD=your_plain_password  # Only used if ADMIN_PASSWORD_HASH not set

# Session Security
SESSION_TIMEOUT=3600  # Session timeout in seconds (default: 1 hour)

# CORS and Domain Control
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
AUTHORIZED_DOMAINS=yourdomain.com,api.yourdomain.com

# Environment
ENVIRONMENT=production  # Disables debug mode and API docs
```

**Environment Variable Details:**
- `ADMIN_USERNAME`: Admin login username (default: 'admin')
- `ADMIN_PASSWORD_HASH`: bcrypt hash of admin password (required for security)
- `ADMIN_PASSWORD`: Fallback plain password (only if hash not provided, NOT recommended)
- `SESSION_TIMEOUT`: Session expiration time in seconds (default: 3600)
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins
- `AUTHORIZED_DOMAINS`: Comma-separated domains that can access API without keys
- `ENVIRONMENT`: Set to 'production' to disable debug features

### Generating Password Hash
Use Python to generate a bcrypt hash for your admin password:

```python
import bcrypt
password = "your_secure_password"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

### API Key Management Workflow
1. Login to admin panel at `/admin`
2. Navigate to the "API Keys" section
3. Fill in the API key creation form:
   - **Name**: Descriptive name for the key
   - **Description**: Optional details about usage
   - **Per-minute limit**: Maximum requests per minute
   - **Daily limit**: Maximum requests per day
   - **Monthly limit**: Maximum requests per month
4. Click "Create API Key" to generate the key
5. Distribute keys securely to authorized users
6. Monitor usage and adjust limits as needed
7. Revoke keys when no longer needed

## Supported Ayanamsha Systems

The application supports 40+ ayanamsha systems including:

**Popular Systems:**
- **J.N. Bhasin** (default) - Precise astronomical calculation system
- **Krishnamurti** (fallback) - Used in KP astrology system  
- **Lahiri** - Most widely used in Indian astrology
- **Raman** - B.V. Raman's ayanamsha
- **Yukteshwar** - Sri Yukteshwar's calculation

**Traditional Fixed Star Systems:**
- **True Chitrapaksha**, **True Pushya**, **True Revati** - Traditional fixed star calculations
- **Aldebaran at 15° Taurus** - Ancient Babylonian system

**Modern Research Systems:**
- **Galactic Center variations** - Multiple modern galactic alignment systems
- **Babylonian systems** - Historical Mesopotamian calculations
- **J2000, J1900, B1950** - Astronomical epoch-based systems

**Classical Indian Systems:**
- **Aryabhata**, **Suryasiddhanta** - Ancient mathematical treatises
- **Siddhanta Shiromani variations** - Medieval astronomical texts

## Supported House Systems

Choose from multiple house division systems:

- **Equal House** (default) - 30° equal divisions from Ascendant, preferred in traditional Vedic astrology
- **Topocentric** (fallback) - Based on observer's location on Earth's surface
- **Placidus** - Most common in Western and some Vedic traditions
- **Sripati** - Traditional Vedic system with proportional houses

## Technical Specifications

### Astronomical Engine
- **Calculation Library**: Swiss Ephemeris (highest precision available)
- **House Systems**: Placidus, Equal, Topocentric, Sripati
- **Node Calculation**: Mean nodes for Rahu/Ketu (traditional Vedic method)
- **Coordinate System**: 360° longitude system
- **Precision**: 6 decimal places for full precision, 2 for display

### Database & Rate Limiting
- **Database**: SQLite with comprehensive schema for usage tracking
- **Usage Tables**: Separate tracking for per-minute, daily, and monthly usage
- **Atomic Operations**: Thread-safe rate limit checking and incrementing
- **Performance Optimization**: Indexed database queries for fast lookups
- **Automatic Cleanup**: Expired usage records are managed automatically

### Time Handling
- **Input Format**: Local time with timezone specification
- **Internal Processing**: Automatic conversion to Universal Time (UT)
- **Timezone Support**: Full pytz timezone database
- **Accuracy**: Second-level precision for birth time

### Data Format
- **Standard Display**: Rounded to 2 decimal places
- **Full Precision**: 6 decimal places for professional use
- **DMS Format**: Traditional Degrees°Minutes'Seconds" for ayanamsha
- **JSON API**: Structured data suitable for integration
- **Dual Charts**: Separate natal and transit calculations in single response

## Requirements

- Python 3.11+
- FastAPI framework
- Uvicorn ASGI server
- Swiss Ephemeris (pyswisseph)
- bcrypt for password security
- pytz for timezone handling
- SQLite for database operations
- Swiss Ephemeris data files (included)

## Security Features

- **Password Security**: bcrypt hashing with salt
- **Session Management**: Token-based with configurable expiration
- **Rate Limiting**: Database-driven usage tracking and enforcement
- **Access Control**: API key and domain-based authorization
- **Security Headers**: HSTS, CSP, XSS protection, clickjacking prevention
- **CORS Protection**: Configurable cross-origin policies
- **Input Validation**: Comprehensive parameter validation and sanitization
- **Usage Monitoring**: Detailed logging and tracking of API usage

## Production Deployment

1. **Set Environment Variables**: Configure all security settings
2. **Enable HTTPS**: Required for security headers to be effective
3. **Configure CORS**: Set specific allowed origins
4. **Set Up Rate Limits**: Configure appropriate limits for your use case
5. **Monitor Access**: Review API key usage and admin access logs
6. **Regular Updates**: Keep dependencies and ephemeris data current
7. **Database Maintenance**: Monitor database size and performance

## Rate Limiting Best Practices

**For API Keys:**
- **Development**: 60/min, 1,000/day, 30,000/month
- **Production APIs**: 600/min, 10,000/day, 300,000/month
- **Enterprise**: Custom limits based on requirements

**For Domain Authorization:**
- **Personal websites**: 10/min, 100/day, 3,000/month
- **Commercial sites**: 60/min, 1,000/day, 30,000/month
- **High-traffic applications**: Use API keys instead of domain auth

For questions or support, refer to the Swiss Ephemeris documentation and FastAPI guides.