# Vedic Astrology Calculator

A comprehensive FastAPI web application with user-friendly frontend interface for Vedic astrology calculations using Swiss Ephemeris. Features secure admin panel, multiple ayanamsha systems, enhanced precision display, and professional chart calculations.

## Features

### Core Astrology Engine
- **40+ Ayanamsha Systems**: Lahiri, Krishnamurti, Raman, Yukteshwar, and many more
- **9 Vedic Planets**: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu (North Node), Ketu (South Node)
- **High Precision**: Full decimal precision with DMS (Degrees, Minutes, Seconds) format display
- **Swiss Ephemeris**: Professional-grade astronomical calculations with Placidus house system
- **Timezone Support**: Automatic conversion from local time to Universal Time

### User Interface
- **Responsive Frontend**: Modern HTML5/CSS3/JavaScript interface optimized for all devices
- **Interactive Forms**: Date picker, time input, timezone selection, and location coordinates
- **Real-time Results**: Instant chart calculations with copy-to-clipboard functionality
- **Professional Display**: Both simplified (2 decimal) and full precision (6 decimal) planetary positions
- **DMS Format**: Traditional Degrees°Minutes'Seconds" display for ayanamsha values

### Security & Administration
- **Secure Admin Panel**: bcrypt password hashing with session-based authentication
- **API Key Management**: Generate, view, and manage API keys for external access
- **Domain Authorization**: Control which domains can access your API endpoints
- **Security Headers**: HSTS, CSP, XSS protection, and other modern security standards
- **Access Control**: Protected endpoints with proper authentication and authorization

## Quick Start

### 1. Access the Application
The server runs automatically on port 5000. Open your browser and navigate to the frontend interface for easy chart calculations.

### 2. Admin Setup (First Time)
1. Go to `/admin` to access the admin login page
2. **IMPORTANT**: Set secure admin credentials via environment variables before first use
3. Default fallback credentials (if no env vars set): `admin` / `admin123`
4. **CRITICAL**: Configure proper environment variables for production deployment
5. Set up API keys and authorized domains as needed

### 3. Frontend Interface
- Fill in birth details: date, time, location coordinates
- Select your preferred timezone from the dropdown
- Choose from 40+ ayanamsha systems (default: Lahiri)
- Click "Calculate Chart" for instant results
- Use copy buttons to copy specific planetary positions or full JSON

## API Documentation

### Authentication
API endpoints require either:
- **API Key Authentication**: Include `Authorization: Bearer <your_api_key>` header
- **Domain Authorization**: Access from pre-authorized domains (configure via admin panel)

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
- `ayanamsha` (string): Ayanamsha system (default: "lahiri")

**Example:**
```bash
# Without API key (only works from authorized domains)
curl "http://localhost:5000/chart?year=2024&month=9&day=16&hour=12&minute=30&second=15&lat=28.6139&lon=77.2090&tz=Asia/Kolkata&ayanamsha=krishnamurti"

# With API key authentication
curl -H "Authorization: Bearer your_api_key_here" \
     "http://localhost:5000/chart?year=2024&month=9&day=16&hour=12&minute=30&second=15&lat=28.6139&lon=77.2090&tz=Asia/Kolkata&ayanamsha=krishnamurti"
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
  "ayanamsha": "krishnamurti"
}
```

**Enhanced Response:**
```json
{
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
  "ayanamsha_name": "Krishnamurti",
  "ayanamsha_value_decimal": 24.105409,
  "ayanamsha_value_dms": "24°06'19.47\"",
  "timezone_used": "Asia/Kolkata",
  "input_time_ut": 7.004167
}
```

### Additional Endpoints

#### GET /ayanamsha-options
List all available ayanamsha systems.

#### GET /security-status
Security configuration status and system information.

#### GET /health  
Health check endpoint.

#### Admin Endpoints (Protected)
- `GET /admin` - Admin login page
- `POST /admin/login` - Admin authentication  
- `POST /admin/logout` - Logout from current session
- `POST /admin/logout-all` - Emergency logout from all sessions
- `GET /admin/api-keys` - View API keys
- `POST /admin/api-keys` - Generate new API key
- `DELETE /admin/api-keys/{api_key}` - Delete API key
- `GET /admin/domains` - View authorized domains
- `POST /admin/domains` - Add authorized domain
- `DELETE /admin/domains/{domain}` - Remove domain

## Admin Configuration

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

### API Key Management
1. Login to admin panel at `/admin`
2. Navigate to "Manage API Keys"
3. Generate keys for external applications
4. Distribute keys securely to authorized users
5. Revoke keys when no longer needed

## Supported Ayanamsha Systems

The application supports 40+ ayanamsha systems including:
- **Lahiri** (default) - Most widely used in Indian astrology
- **Krishnamurti** - Used in KP astrology system  
- **Raman** - B.V. Raman's ayanamsha
- **Yukteshwar** - Sri Yukteshwar's calculation
- **Fagan Bradley** - Western sidereal standard
- **True Chitrapaksha**, **True Pushya**, **True Revati** - Traditional fixed star calculations
- And many more...

## Technical Specifications

### Astronomical Engine
- **Calculation Library**: Swiss Ephemeris (highest precision available)
- **House System**: Placidus (traditional Vedic standard)
- **Node Calculation**: Mean nodes for Rahu/Ketu (traditional Vedic method)
- **Coordinate System**: 360° longitude system
- **Precision**: 6 decimal places for full precision, 2 for display

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

## Requirements

- Python 3.11+
- FastAPI framework
- Uvicorn ASGI server
- Swiss Ephemeris (pyswisseph)
- bcrypt for password security
- pytz for timezone handling
- Swiss Ephemeris data files (included)

## Security Features

- **Password Security**: bcrypt hashing with salt
- **Session Management**: Token-based with configurable expiration
- **Access Control**: API key and domain-based authorization
- **Security Headers**: HSTS, CSP, XSS protection, clickjacking prevention
- **CORS Protection**: Configurable cross-origin policies
- **Input Validation**: Comprehensive parameter validation and sanitization

## Production Deployment

1. **Set Environment Variables**: Configure all security settings
2. **Enable HTTPS**: Required for security headers to be effective
3. **Configure CORS**: Set specific allowed origins
4. **Monitor Access**: Review API key usage and admin access logs
5. **Regular Updates**: Keep dependencies and ephemeris data current

For questions or support, refer to the Swiss Ephemeris documentation and FastAPI guides.