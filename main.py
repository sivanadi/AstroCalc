from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from enum import Enum
import swisseph as swe
import pytz
import os
import json
import secrets
from datetime import datetime, timedelta
from typing import Dict, Union, Optional, List
import hashlib
import bcrypt
import sqlite3

app = FastAPI(
    title="Vedic Astrology Calculator", 
    description="Calculate planetary longitudes and Ascendant using Swiss Ephemeris",
    # Security: Hide server information
    redoc_url=None if os.getenv('ENVIRONMENT') == 'production' else '/redoc',
    docs_url=None if os.getenv('ENVIRONMENT') == 'production' else '/docs'
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("Initializing database...")
    init_database()
    
    # Validate security configuration
    validate_security_config()
    
    # Create admin user securely if needed
    try:
        create_admin_if_needed()
    except ValueError as e:
        print(f"CRITICAL SECURITY ERROR: {e}")
        print("Application cannot start without proper admin configuration")
        os._exit(1)  # Force exit on security error
    
    migrate_existing_data()
    add_database_indexes()
    print("Database initialization completed")

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Security headers to prevent common attacks
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    
    # Remove server header for security
    if "server" in response.headers:
        del response.headers["server"]
    
    return response

# CORS configuration - restrictive by default
# Include Replit preview domain in CORS origins
replit_dev_domain = os.getenv('REPLIT_DEV_DOMAIN', '')
default_cors_origins = ['http://localhost:5000']
if replit_dev_domain:
    default_cors_origins.append(f'https://{replit_dev_domain}')
allowed_origins = os.getenv('CORS_ORIGINS', ','.join(default_cors_origins)).split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

security = HTTPBearer(auto_error=False)

# Set the ephemeris path
ephe_path = os.path.join(os.getcwd(), "ephe")
swe.set_ephe_path(ephe_path)

# Ayanamsha options
AYANAMSHA_OPTIONS = {
    'lahiri': {'id': swe.SIDM_LAHIRI, 'name': 'N.C. Lahiri'},
    'raman': {'id': swe.SIDM_RAMAN, 'name': 'B.V. Raman'},
    'krishnamurti': {'id': swe.SIDM_KRISHNAMURTI, 'name': 'Krishnamurti'},
    'yukteshwar': {'id': swe.SIDM_YUKTESHWAR, 'name': 'Yukteshwar'},
    'jn_bhasin': {'id': swe.SIDM_JN_BHASIN, 'name': 'J.N. Bhasin'},
    'babyl_kugler1': {'id': swe.SIDM_BABYL_KUGLER1, 'name': 'Babylonian (Kugler 1)'},
    'babyl_kugler2': {'id': swe.SIDM_BABYL_KUGLER2, 'name': 'Babylonian (Kugler 2)'},
    'babyl_kugler3': {'id': swe.SIDM_BABYL_KUGLER3, 'name': 'Babylonian (Kugler 3)'},
    'babyl_huber': {'id': swe.SIDM_BABYL_HUBER, 'name': 'Babylonian (Huber)'},
    'babyl_etpsc': {'id': swe.SIDM_BABYL_ETPSC, 'name': 'Babylonian (ETPSC)'},
    'aldebaran_15tau': {'id': swe.SIDM_ALDEBARAN_15TAU, 'name': 'Aldebaran at 15° Taurus'},
    'hipparchos': {'id': swe.SIDM_HIPPARCHOS, 'name': 'Hipparchos'},
    'sassanian': {'id': swe.SIDM_SASSANIAN, 'name': 'Sassanian'},
    'galcent_0sag': {'id': swe.SIDM_GALCENT_0SAG, 'name': 'Galactic Center at 0° Sagittarius'},
    'j2000': {'id': swe.SIDM_J2000, 'name': 'J2000'},
    'j1900': {'id': swe.SIDM_J1900, 'name': 'J1900'},
    'b1950': {'id': swe.SIDM_B1950, 'name': 'B1950'},
    'suryasiddhanta': {'id': swe.SIDM_SURYASIDDHANTA, 'name': 'Suryasiddhanta'},
    'suryasiddhanta_msun': {'id': swe.SIDM_SURYASIDDHANTA_MSUN, 'name': 'Suryasiddhanta (Mean Sun)'},
    'aryabhata': {'id': swe.SIDM_ARYABHATA, 'name': 'Aryabhata'},
    'aryabhata_msun': {'id': swe.SIDM_ARYABHATA_MSUN, 'name': 'Aryabhata (Mean Sun)'},
    'ss_revati': {'id': swe.SIDM_SS_REVATI, 'name': 'Siddhanta Shiromani (Revati)'},
    'ss_citra': {'id': swe.SIDM_SS_CITRA, 'name': 'Siddhanta Shiromani (Citra)'},
    'true_citra': {'id': swe.SIDM_TRUE_CITRA, 'name': 'True Citra'},
    'true_revati': {'id': swe.SIDM_TRUE_REVATI, 'name': 'True Revati'},
    'true_pushya': {'id': swe.SIDM_TRUE_PUSHYA, 'name': 'True Pushya'},
    'galcent_rgilbrand': {'id': swe.SIDM_GALCENT_RGILBRAND, 'name': 'Galactic Center (Gil Brand)'},
    'galequ_iau1958': {'id': swe.SIDM_GALEQU_IAU1958, 'name': 'Galactic Equator IAU1958'},
    'galequ_true': {'id': swe.SIDM_GALEQU_TRUE, 'name': 'Galactic Equator True'},
    'galequ_mula': {'id': swe.SIDM_GALEQU_MULA, 'name': 'Galactic Equator at Mula'},
    'galalign_mardyks': {'id': swe.SIDM_GALALIGN_MARDYKS, 'name': 'Galactic Alignment (Mardyks)'},
    'true_mula': {'id': swe.SIDM_TRUE_MULA, 'name': 'True Mula'},
    'galcent_mula_wilhelm': {'id': swe.SIDM_GALCENT_MULA_WILHELM, 'name': 'Galactic Center at Mula (Wilhelm)'},
    'aryabhata_522': {'id': swe.SIDM_ARYABHATA_522, 'name': 'Aryabhata 522'},
    'babyl_britton': {'id': swe.SIDM_BABYL_BRITTON, 'name': 'Babylonian (Britton)'},
    'true_sheoran': {'id': swe.SIDM_TRUE_SHEORAN, 'name': 'True Sheoran'},
    'galcent_cochrane': {'id': swe.SIDM_GALCENT_COCHRANE, 'name': 'Galactic Center (Cochrane)'},
    'galequ_fiorenza': {'id': swe.SIDM_GALEQU_FIORENZA, 'name': 'Galactic Equator (Fiorenza)'},
    'valens_moon': {'id': swe.SIDM_VALENS_MOON, 'name': 'Valens (Moon)'}
}

# Default to Lahiri
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Planet constants for Swiss Ephemeris
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON, 
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,  # Mean North Node
}

# House system options for Swiss Ephemeris
HOUSE_SYSTEMS = {
    'placidus': 'P',        # Placidus
    'equal': 'E',           # Equal House
    'topocentric': 'T',     # Topocentric (Poli)
    'sripati': 'S'          # Sripati
}

HOUSE_SYSTEM_NAMES = {
    'placidus': 'Placidus',
    'equal': 'Equal House', 
    'topocentric': 'Topocentric',
    'sripati': 'Sripati'
}

# Admin authentication is now handled entirely through the database
# No environment variables are used for admin credentials for security

# Session timeout in seconds (default: 1 hour)
SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))

# Restrictive default domains - only localhost by default for development
# Production should use environment variable AUTHORIZED_DOMAINS or database entries
default_domains_list = ['localhost', '127.0.0.1']
default_domains = os.getenv('AUTHORIZED_DOMAINS', ','.join(default_domains_list))
AUTHORIZED_DOMAINS = set(domain.strip() for domain in default_domains.split(',') if domain.strip())
API_KEYS = {}
ACTIVE_SESSIONS = {}  # Now stores {token: {username: str, created_at: datetime}}

# Request models
class ChartRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int  # Changed to int for proper separation
    minute: int = 0  # Added minute field
    second: int = 0  # Added second field
    lat: float
    lon: float
    tz: str = 'UTC'
    # Legacy fields - kept for backward compatibility
    ayanamsha: str = 'lahiri'  # Will be used as fallback if natal/transit specific ones not provided
    house_system: str = 'placidus'  # Will be used as fallback if natal/transit specific ones not provided
    # New separate fields - optional to maintain backward compatibility
    natal_ayanamsha: Optional[str] = None  # Separate ayanamsha for natal calculations
    natal_house_system: Optional[str] = None  # Separate house system for natal calculations
    transit_ayanamsha: Optional[str] = None  # Separate ayanamsha for transit calculations
    transit_house_system: Optional[str] = None  # Separate house system for transit calculations

class AdminLogin(BaseModel):
    username: str
    password: str

class APIKeyRequest(BaseModel):
    name: str
    description: Optional[str] = ''

class DomainRequest(BaseModel):
    domain: str

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

class UpdateAPIKeyLimitsRequest(BaseModel):
    per_minute_limit: int = 60
    per_day_limit: int = 1000
    per_month_limit: int = 30000

class UpdateDomainLimitsRequest(BaseModel):
    per_minute_limit: int = 10
    per_day_limit: int = 100
    per_month_limit: int = 3000

class CreateAPIKeyRequest(BaseModel):
    name: str
    description: Optional[str] = ''
    per_minute_limit: int = 60
    per_day_limit: int = 1000
    per_month_limit: int = 30000

class CreateDomainRequest(BaseModel):
    domain: str
    per_minute_limit: int = 10
    per_day_limit: int = 100
    per_month_limit: int = 3000

# Security Enums for V1 Admin API
class APIKeySortField(str, Enum):
    id = "id"
    key_name = "name"
    created_at = "created_at"
    updated_at = "updated_at"
    per_minute_limit = "per_minute_limit"
    per_day_limit = "per_day_limit"
    per_month_limit = "per_month_limit"

class DomainSortField(str, Enum):
    id = "id"
    domain = "domain"
    created_at = "created_at"
    updated_at = "updated_at"
    per_minute_limit = "per_minute_limit"
    per_day_limit = "per_day_limit"
    per_month_limit = "per_month_limit"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class BulkOperationType(str, Enum):
    delete = "delete"
    activate = "activate"
    deactivate = "deactivate"
    update_limits = "update_limits"

# Payload validation for update_limits operation
class BulkUpdateLimitsPayload(BaseModel):
    per_minute_limit: Optional[int] = Field(None, ge=1, le=10000)
    per_day_limit: Optional[int] = Field(None, ge=1, le=1000000)
    per_month_limit: Optional[int] = Field(None, ge=1, le=50000000)

    @validator('per_minute_limit', 'per_day_limit', 'per_month_limit', pre=True)
    def validate_positive_integers(cls, v):
        if v is not None:
            if not isinstance(v, int) or v <= 0:
                raise ValueError('Limit values must be positive integers')
        return v

# V1 Admin API Models - Enhanced for scalability
class APIKeyPaginationParams(BaseModel):
    page: int = Field(1, ge=1, le=10000)
    page_size: int = Field(25, ge=1, le=1000)
    search: Optional[str] = Field("", max_length=255)
    sort_by: APIKeySortField = APIKeySortField.created_at
    sort_order: SortOrder = SortOrder.desc

class DomainPaginationParams(BaseModel):
    page: int = Field(1, ge=1, le=10000)
    page_size: int = Field(25, ge=1, le=1000)
    search: Optional[str] = Field("", max_length=255)
    sort_by: DomainSortField = DomainSortField.created_at
    sort_order: SortOrder = SortOrder.desc

class APIKeyFilters(BaseModel):
    is_active: Optional[bool] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None

    @validator('created_after', 'created_before', pre=True)
    def validate_datetime_strings(cls, v):
        if v is not None and isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Date must be in ISO format (YYYY-MM-DDTHH:MM:SS)')
        return v

class DomainFilters(BaseModel):
    is_active: Optional[bool] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None

    @validator('created_after', 'created_before', pre=True)
    def validate_datetime_strings(cls, v):
        if v is not None and isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Date must be in ISO format (YYYY-MM-DDTHH:MM:SS)')
        return v

class BulkOperation(BaseModel):
    operation: BulkOperationType
    ids: List[int]
    payload: Optional[BulkUpdateLimitsPayload] = None

    @validator('ids')
    def validate_ids_list(cls, v):
        if not v or len(v) == 0:
            raise ValueError('At least one ID must be provided')
        if len(v) > 1000:
            raise ValueError('Cannot process more than 1000 items at once')
        return v
    
    @validator('payload')
    def validate_payload_for_operation(cls, v, values):
        operation = values.get('operation')
        if operation == BulkOperationType.update_limits:
            if v is None:
                raise ValueError('Payload is required for update_limits operation')
            if not any([v.per_minute_limit is not None, v.per_day_limit is not None, v.per_month_limit is not None]):
                raise ValueError('At least one limit must be specified in payload')
        elif v is not None:
            raise ValueError(f'Payload not allowed for {operation} operation')
        return v

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

class APIKeyResponse(BaseModel):
    id: int
    key_hash: str
    name: str
    description: str
    per_minute_limit: int
    per_day_limit: int
    per_month_limit: int
    is_active: bool
    created_at: str
    updated_at: str

class DomainResponse(BaseModel):
    id: int
    domain: str
    per_minute_limit: int
    per_day_limit: int
    per_month_limit: int
    is_active: bool
    created_at: str
    updated_at: str


# Utility functions
def decimal_to_dms(decimal_degrees):
    """Convert decimal degrees to degrees, minutes, seconds format"""
    degrees = int(decimal_degrees)
    minutes_float = (decimal_degrees - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60
    return f"{degrees}°{minutes:02d}'{seconds:05.2f}\""

def convert_timezone_to_ut(year, month, day, hour, minute, second, timezone_str):
    """Convert local time to Universal Time"""
    try:
        if timezone_str == 'UTC':
            return hour + minute/60 + second/3600
        
        tz = pytz.timezone(timezone_str)
        local_dt = datetime(year, month, day, int(hour), int(minute), int(second))
        local_dt = tz.localize(local_dt)
        utc_dt = local_dt.astimezone(pytz.UTC)
        
        return utc_dt.hour + utc_dt.minute/60 + utc_dt.second/3600
    except:
        # If timezone conversion fails, assume UTC
        return hour + minute/60 + second/3600

def convert_julian_to_date(julian_day_ut, timezone_str='UTC'):
    """Convert Julian Day to readable date format like '21 July 1986 time: 17:45:23'"""
    try:
        # Convert Julian Day to calendar date using Swiss Ephemeris
        year, month, day, hour_ut = swe.revjul(julian_day_ut)
        
        # Convert decimal hour to hours, minutes, seconds
        hours = int(hour_ut)
        minutes = int((hour_ut - hours) * 60)
        seconds = int(((hour_ut - hours) * 60 - minutes) * 60)
        
        # Create datetime object in UTC
        utc_dt = datetime(int(year), int(month), int(day), hours, minutes, seconds)
        
        # Convert to user's timezone if not UTC
        if timezone_str != 'UTC':
            try:
                tz = pytz.timezone(timezone_str)
                utc_dt = pytz.UTC.localize(utc_dt)
                local_dt = utc_dt.astimezone(tz)
            except:
                local_dt = utc_dt
        else:
            local_dt = utc_dt
        
        # Format as "21 July 1986 time: 17:45:23"
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        formatted_date = f"{local_dt.day} {month_names[local_dt.month]} {local_dt.year} time: {local_dt.hour:02d}:{local_dt.minute:02d}:{local_dt.second:02d}"
        
        return formatted_date
        
    except Exception as e:
        # Fallback format if conversion fails
        return f"Julian Day: {julian_day_ut}"

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    # Create admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            must_change_password BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create api_keys table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_hash TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            per_minute_limit INTEGER DEFAULT 60,
            per_day_limit INTEGER DEFAULT 1000,
            per_month_limit INTEGER DEFAULT 30000,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create authorized_domains table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authorized_domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT UNIQUE NOT NULL,
            per_minute_limit INTEGER DEFAULT 10,
            per_day_limit INTEGER DEFAULT 100,
            per_month_limit INTEGER DEFAULT 3000,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create usage tracking tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_minute (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifier TEXT NOT NULL,
            identifier_type TEXT NOT NULL CHECK(identifier_type IN ('api_key', 'domain')),
            minute_key TEXT NOT NULL,
            count INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(identifier, identifier_type, minute_key)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_day (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifier TEXT NOT NULL,
            identifier_type TEXT NOT NULL CHECK(identifier_type IN ('api_key', 'domain')),
            day_key TEXT NOT NULL,
            count INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(identifier, identifier_type, day_key)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_month (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifier TEXT NOT NULL,
            identifier_type TEXT NOT NULL CHECK(identifier_type IN ('api_key', 'domain')),
            month_key TEXT NOT NULL,
            count INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(identifier, identifier_type, month_key)
        )
    ''')
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usage_minute_identifier ON usage_minute(identifier, minute_key)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usage_day_identifier ON usage_day(identifier, day_key)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usage_month_identifier ON usage_month(identifier, month_key)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON api_keys(key_hash)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_domains_domain ON authorized_domains(domain)')
    
    conn.commit()
    conn.close()

def add_database_indexes():
    """Add additional performance indexes for v1 admin queries"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # Additional indexes for improved v1 admin query performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_keys_is_active ON api_keys(is_active)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_keys_created_at ON api_keys(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_keys_updated_at ON api_keys(updated_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_keys_name ON api_keys(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_keys_per_minute_limit ON api_keys(per_minute_limit)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_keys_per_day_limit ON api_keys(per_day_limit)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_keys_per_month_limit ON api_keys(per_month_limit)')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_domains_is_active ON authorized_domains(is_active)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_domains_created_at ON authorized_domains(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_domains_updated_at ON authorized_domains(updated_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_domains_per_minute_limit ON authorized_domains(per_minute_limit)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_domains_per_day_limit ON authorized_domains(per_day_limit)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_domains_per_month_limit ON authorized_domains(per_month_limit)')
        
        # Composite indexes for common filter combinations
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_keys_active_created ON api_keys(is_active, created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_domains_active_created ON authorized_domains(is_active, created_at)')
        
        conn.commit()
        conn.close()
        print("Database performance indexes added successfully")
        return True
        
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error adding indexes: {e}")
        return False

def create_admin_if_needed():
    """Create admin user with secure password from environment variable"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # Check if admin already exists
        cursor.execute('SELECT COUNT(*) FROM admins WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            # Get admin password from environment variable
            admin_password = os.getenv('ADMIN_PASSWORD')
            if not admin_password:
                print("ERROR: ADMIN_PASSWORD environment variable is required to create admin user")
                print("Please set ADMIN_PASSWORD environment variable and restart the application")
                raise ValueError("Missing ADMIN_PASSWORD environment variable")
            
            if len(admin_password) < 8:
                print("ERROR: ADMIN_PASSWORD must be at least 8 characters long")
                raise ValueError("ADMIN_PASSWORD too short")
            
            # Create admin user with secure password from environment
            password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute(
                'INSERT INTO admins (username, password_hash, must_change_password) VALUES (?, ?, ?)',
                ('admin', password_hash, True)
            )
            print("Admin user created successfully with environment-provided password")
            print("NOTE: Admin must change password on first login")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Admin creation error: {e}")
        conn.rollback()
        conn.close()
        raise

def migrate_existing_data():
    """Migrate existing in-memory data to database"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # Migrate existing API keys from in-memory storage
        for key_hash, key_data in API_KEYS.items():
            cursor.execute('SELECT COUNT(*) FROM api_keys WHERE key_hash = ?', (key_hash,))
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO api_keys (key_hash, name, description) 
                    VALUES (?, ?, ?)
                ''', (key_hash, key_data.get('name', ''), key_data.get('description', '')))
        
        # Migrate existing authorized domains
        for domain in AUTHORIZED_DOMAINS:
            cursor.execute('SELECT COUNT(*) FROM authorized_domains WHERE domain = ?', (domain,))
            if cursor.fetchone()[0] == 0:
                cursor.execute('INSERT INTO authorized_domains (domain) VALUES (?)', (domain,))
        
        conn.commit()
        print("Database migration completed successfully")
        
    except Exception as e:
        print(f"Database migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

# Database helper functions
def validate_security_config():
    """Validate security configuration at startup"""
    # Check if admin password is set in environment when no admin exists
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM admins WHERE username = ?', ('admin',))
    admin_exists = cursor.fetchone()[0] > 0
    conn.close()
    
    if not admin_exists:
        admin_password = os.getenv('ADMIN_PASSWORD')
        if not admin_password:
            print("SECURITY ERROR: No admin user exists and ADMIN_PASSWORD environment variable is not set")
            print("Set ADMIN_PASSWORD environment variable to create the initial admin user")
            raise ValueError("Missing ADMIN_PASSWORD environment variable for initial setup")
        
        if len(admin_password) < 8:
            print("SECURITY ERROR: ADMIN_PASSWORD must be at least 8 characters long")
            raise ValueError("ADMIN_PASSWORD too short (minimum 8 characters required)")
    
    print("Security configuration validated successfully")

def get_admin_by_username(username: str):
    """Get admin user by username"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admins WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'id': result[0],
            'username': result[1], 
            'password_hash': result[2],
            'must_change_password': bool(result[3]) if len(result) > 3 else False,
            'created_at': result[4] if len(result) > 4 else result[3],
            'updated_at': result[5] if len(result) > 5 else result[4] if len(result) > 4 else result[3]
        }
    return None

def update_admin_password(username: str, new_password_hash: str, clear_change_requirement: bool = True):
    """Update admin password and optionally clear password change requirement"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    if clear_change_requirement:
        cursor.execute(
            'UPDATE admins SET password_hash = ?, must_change_password = FALSE, updated_at = CURRENT_TIMESTAMP WHERE username = ?',
            (new_password_hash, username)
        )
    else:
        cursor.execute(
            'UPDATE admins SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?',
            (new_password_hash, username)
        )
    
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def get_api_keys_paginated(page: int = 1, page_size: int = 20, search: str = ''):
    """Get API keys with pagination and search"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    offset = (page - 1) * page_size
    search_pattern = f'%{search}%'
    
    # Get total count
    cursor.execute(
        'SELECT COUNT(*) FROM api_keys WHERE name LIKE ? OR description LIKE ?',
        (search_pattern, search_pattern)
    )
    total = cursor.fetchone()[0]
    
    # Get paginated results
    cursor.execute('''
        SELECT key_hash, name, description, per_minute_limit, per_day_limit, per_month_limit, 
               is_active, created_at, updated_at
        FROM api_keys 
        WHERE name LIKE ? OR description LIKE ?
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    ''', (search_pattern, search_pattern, page_size, offset))
    
    keys = []
    for row in cursor.fetchall():
        keys.append({
            'key_hash': row[0],
            'name': row[1],
            'description': row[2],
            'per_minute_limit': row[3],
            'per_day_limit': row[4],
            'per_month_limit': row[5],
            'is_active': bool(row[6]),
            'created_at': row[7],
            'updated_at': row[8]
        })
    
    conn.close()
    return {
        'keys': keys,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    }

def create_api_key_db(name: str, description: str = '', per_minute_limit: int = 60, 
                     per_day_limit: int = 1000, per_month_limit: int = 30000):
    """Create new API key in database"""
    api_key = secrets.token_urlsafe(32)
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO api_keys (key_hash, name, description, per_minute_limit, per_day_limit, per_month_limit)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (key_hash, name, description, per_minute_limit, per_day_limit, per_month_limit))
        conn.commit()
        conn.close()
        return {'api_key': api_key, 'key_hash': key_hash}
    except sqlite3.IntegrityError:
        conn.close()
        return None

def update_api_key_limits(key_hash: str, per_minute_limit: int, per_day_limit: int, per_month_limit: int):
    """Update API key limits"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE api_keys 
        SET per_minute_limit = ?, per_day_limit = ?, per_month_limit = ?, updated_at = CURRENT_TIMESTAMP
        WHERE key_hash = ?
    ''', (per_minute_limit, per_day_limit, per_month_limit, key_hash))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def delete_api_key_db(key_hash: str):
    """Delete API key from database"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM api_keys WHERE key_hash = ?', (key_hash,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def get_authorized_domains():
    """Get all authorized domains"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM authorized_domains WHERE is_active = TRUE ORDER BY created_at DESC')
    domains = []
    for row in cursor.fetchall():
        domains.append({
            'id': row[0],
            'domain': row[1],
            'per_minute_limit': row[2],
            'per_day_limit': row[3], 
            'per_month_limit': row[4],
            'is_active': bool(row[5]),
            'created_at': row[6],
            'updated_at': row[7]
        })
    conn.close()
    return domains

def add_authorized_domain(domain: str, per_minute_limit: int = 10, per_day_limit: int = 100, per_month_limit: int = 3000):
    """Add authorized domain"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO authorized_domains (domain, per_minute_limit, per_day_limit, per_month_limit)
            VALUES (?, ?, ?, ?)
        ''', (domain, per_minute_limit, per_day_limit, per_month_limit))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def delete_authorized_domain(domain: str):
    """Delete authorized domain"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM authorized_domains WHERE domain = ?', (domain,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

# Rate limiting functions
def get_time_keys():
    """Get current minute, day, and month keys for rate limiting"""
    now = datetime.now()
    minute_key = now.strftime('%Y-%m-%d-%H-%M')
    day_key = now.strftime('%Y-%m-%d')
    month_key = now.strftime('%Y-%m')
    return minute_key, day_key, month_key

def check_and_increment_usage(identifier: str, identifier_type: str, per_minute_limit: int, per_day_limit: int, per_month_limit: int):
    """Check rate limits and increment usage counters atomically"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    minute_key, day_key, month_key = get_time_keys()
    now = datetime.now()
    
    try:
        # Check current usage
        cursor.execute('SELECT count FROM usage_minute WHERE identifier = ? AND minute_key = ?', (identifier, minute_key))
        minute_count = cursor.fetchone()
        minute_count = minute_count[0] if minute_count else 0
        
        cursor.execute('SELECT count FROM usage_day WHERE identifier = ? AND day_key = ?', (identifier, day_key))
        day_count = cursor.fetchone()
        day_count = day_count[0] if day_count else 0
        
        cursor.execute('SELECT count FROM usage_month WHERE identifier = ? AND month_key = ?', (identifier, month_key))
        month_count = cursor.fetchone()
        month_count = month_count[0] if month_count else 0
        
        # Check limits with enhanced user-friendly messages
        if minute_count >= per_minute_limit:
            conn.close()
            seconds_remaining = 60 - now.second
            return False, f"Per-minute limit exceeded: {minute_count}/{per_minute_limit}. You have reached your maximum requests per minute. Please wait {seconds_remaining} seconds before making your next request."
        
        if day_count >= per_day_limit:
            conn.close()
            next_day = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            hours_remaining = int((next_day - now).total_seconds() // 3600)
            minutes_remaining = int(((next_day - now).total_seconds() % 3600) // 60)
            return False, f"Daily limit exceeded: {day_count}/{per_day_limit}. You have reached your maximum requests for today. Your limit will reset in {hours_remaining} hours and {minutes_remaining} minutes."
        
        if month_count >= per_month_limit:
            conn.close()
            if now.month == 12:
                next_month = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                next_month = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
            days_remaining = (next_month - now).days
            return False, f"Monthly limit exceeded: {month_count}/{per_month_limit}. You have reached your maximum requests for this month. Your limit will reset in {days_remaining} days."
        
        # Increment counters atomically
        cursor.execute('''
            INSERT INTO usage_minute (identifier, identifier_type, minute_key, count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(identifier, minute_key) DO UPDATE SET count = count + 1
        ''', (identifier, identifier_type, minute_key))
        
        cursor.execute('''
            INSERT INTO usage_day (identifier, identifier_type, day_key, count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(identifier, day_key) DO UPDATE SET count = count + 1
        ''', (identifier, identifier_type, day_key))
        
        cursor.execute('''
            INSERT INTO usage_month (identifier, identifier_type, month_key, count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(identifier, month_key) DO UPDATE SET count = count + 1
        ''', (identifier, identifier_type, month_key))
        
        conn.commit()
        conn.close()
        return True, "Usage incremented successfully"
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Database error: {str(e)}"

def get_api_key_limits(key_hash: str):
    """Get API key limits from database"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT per_minute_limit, per_day_limit, per_month_limit, is_active 
        FROM api_keys WHERE key_hash = ?
    ''', (key_hash,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'per_minute_limit': result[0],
            'per_day_limit': result[1], 
            'per_month_limit': result[2],
            'is_active': bool(result[3])
        }
    return None

def get_domain_limits(domain: str):
    """Get domain limits from database"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT per_minute_limit, per_day_limit, per_month_limit, is_active 
        FROM authorized_domains WHERE domain = ?
    ''', (domain,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'per_minute_limit': result[0],
            'per_day_limit': result[1],
            'per_month_limit': result[2], 
            'is_active': bool(result[3])
        }
    return None

# Analytics functions
def get_usage_analytics(days: int = 30, view_type: str = "all", identifier: Optional[str] = None, period: Optional[str] = None):
    """Get comprehensive usage analytics for the last N days
    
    Args:
        days: Number of days to analyze
        view_type: Filter by 'all', 'api_key', or 'domain'
        identifier: Optional specific API key hash or domain to filter by
        period: Special period handling ('today', 'yesterday', or None for normal days)
    """
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    # Calculate date range based on period
    if period == "today":
        start_date = end_date = datetime.now().date()
    elif period == "yesterday":
        start_date = end_date = datetime.now().date() - timedelta(days=1)
    else:
        # Standard date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
    
    try:
        # Get daily usage for line chart
        if identifier:
            # Filter by specific identifier
            cursor.execute('''
                SELECT day_key, 
                       identifier_type,
                       SUM(count) as total_requests
                FROM usage_day 
                WHERE day_key >= ? AND day_key <= ? AND identifier = ?
                GROUP BY day_key, identifier_type
                ORDER BY day_key
            ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), identifier))
        elif view_type == "all":
            cursor.execute('''
                SELECT day_key, 
                       identifier_type,
                       SUM(count) as total_requests
                FROM usage_day 
                WHERE day_key >= ? AND day_key <= ?
                GROUP BY day_key, identifier_type
                ORDER BY day_key
            ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        else:
            cursor.execute('''
                SELECT day_key, 
                       identifier_type,
                       SUM(count) as total_requests
                FROM usage_day 
                WHERE day_key >= ? AND day_key <= ? AND identifier_type = ?
                GROUP BY day_key, identifier_type
                ORDER BY day_key
            ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), view_type))
        
        daily_usage_raw = cursor.fetchall()
        
        # Process daily usage data
        daily_usage = {}
        for row in daily_usage_raw:
            day_key, identifier_type, count = row
            if day_key not in daily_usage:
                daily_usage[day_key] = {'api_key': 0, 'domain': 0, 'total': 0}
            daily_usage[day_key][identifier_type] = count
            daily_usage[day_key]['total'] += count
        
        # Fill in missing days with zeros
        current_date = start_date
        while current_date <= end_date:
            day_key = current_date.strftime('%Y-%m-%d')
            if day_key not in daily_usage:
                daily_usage[day_key] = {'api_key': 0, 'domain': 0, 'total': 0}
            current_date += timedelta(days=1)
        
        # Get total statistics
        if identifier:
            # For specific identifier, get stats for that identifier only
            cursor.execute('''
                SELECT identifier_type, 
                       SUM(count) as total_requests,
                       COUNT(DISTINCT identifier) as unique_identifiers
                FROM usage_day 
                WHERE day_key >= ? AND day_key <= ? AND identifier = ?
                GROUP BY identifier_type
            ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), identifier))
        elif view_type == "all":
            cursor.execute('''
                SELECT identifier_type, 
                       SUM(count) as total_requests,
                       COUNT(DISTINCT identifier) as unique_identifiers
                FROM usage_day 
                WHERE day_key >= ? AND day_key <= ?
                GROUP BY identifier_type
            ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        else:
            cursor.execute('''
                SELECT identifier_type, 
                       SUM(count) as total_requests,
                       COUNT(DISTINCT identifier) as unique_identifiers
                FROM usage_day 
                WHERE day_key >= ? AND day_key <= ? AND identifier_type = ?
                GROUP BY identifier_type
            ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), view_type))
        
        totals_raw = cursor.fetchall()
        totals = {'api_key': {'requests': 0, 'unique': 0}, 'domain': {'requests': 0, 'unique': 0}}
        
        for row in totals_raw:
            identifier_type, total_requests, unique_identifiers = row
            totals[identifier_type] = {'requests': total_requests, 'unique': unique_identifiers}
        
        # Get top API keys by usage (only if view_type allows)
        top_api_keys = []
        if identifier and view_type == "api_key":
            # For specific API key, show just that key
            cursor.execute('''
                SELECT ak.name, ak.description, SUM(ud.count) as total_requests
                FROM usage_day ud
                JOIN api_keys ak ON ud.identifier = ak.key_hash
                WHERE ud.day_key >= ? AND ud.day_key <= ? AND ud.identifier = ? AND ud.identifier_type = 'api_key'
                GROUP BY ud.identifier, ak.name, ak.description
                ORDER BY total_requests DESC
            ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), identifier))
        elif not identifier and view_type in ["all", "api_key"]:
            cursor.execute('''
                SELECT ak.name, ak.description, SUM(ud.count) as total_requests
                FROM usage_day ud
                JOIN api_keys ak ON ud.identifier = ak.key_hash
                WHERE ud.day_key >= ? AND ud.day_key <= ? AND ud.identifier_type = 'api_key'
                GROUP BY ud.identifier, ak.name, ak.description
                ORDER BY total_requests DESC
                LIMIT 10
            ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
            
            for row in cursor.fetchall():
                name, description, requests = row
                top_api_keys.append({
                    'name': name,
                    'description': description or 'No description',
                    'requests': requests
                })
        
        # Get top domains by usage (only if view_type allows)
        top_domains = []
        if identifier and view_type == "domain":
            # For specific domain, show just that domain
            cursor.execute('''
                SELECT ad.domain, ad.description, SUM(ud.count) as total_requests
                FROM usage_day ud
                JOIN authorized_domains ad ON ud.identifier = ad.domain
                WHERE ud.day_key >= ? AND ud.day_key <= ? AND ud.identifier = ? AND ud.identifier_type = 'domain'
                GROUP BY ud.identifier, ad.domain, ad.description
                ORDER BY total_requests DESC
            ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), identifier))
        elif not identifier and view_type in ["all", "domain"]:
            cursor.execute('''
                SELECT ad.domain, ad.description, SUM(ud.count) as total_requests
                FROM usage_day ud
                JOIN authorized_domains ad ON ud.identifier = ad.domain
                WHERE ud.day_key >= ? AND ud.day_key <= ? AND ud.identifier_type = 'domain'
                GROUP BY ud.identifier, ad.domain, ad.description
                ORDER BY total_requests DESC
                LIMIT 10
            ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
            
            for row in cursor.fetchall():
                domain, description, requests = row
                top_domains.append({
                    'domain': domain,
                    'description': description or 'No description',
                    'requests': requests
                })
        
        # Get hourly distribution (for current day)
        today = datetime.now().strftime('%Y-%m-%d')
        if identifier:
            # For specific identifier, get hourly data for that identifier
            cursor.execute('''
                SELECT SUBSTR(minute_key, 12, 2) as hour, SUM(count) as requests
                FROM usage_minute
                WHERE minute_key LIKE ? || '%' AND identifier = ?
                GROUP BY hour
                ORDER BY hour
            ''', (today, identifier))
        elif view_type == "all":
            cursor.execute('''
                SELECT SUBSTR(minute_key, 12, 2) as hour, SUM(count) as requests
                FROM usage_minute
                WHERE minute_key LIKE ? || '%'
                GROUP BY hour
                ORDER BY hour
            ''', (today,))
        else:
            # For filtered views, get hourly data only for the selected type
            cursor.execute('''
                SELECT SUBSTR(minute_key, 12, 2) as hour, SUM(count) as requests
                FROM usage_minute
                WHERE minute_key LIKE ? || '%' AND identifier_type = ?
                GROUP BY hour
                ORDER BY hour
            ''', (today, view_type))
        
        hourly_distribution = {}
        for row in cursor.fetchall():
            hour, requests = row
            hourly_distribution[int(hour)] = requests
        
        # Fill in missing hours with zeros
        for hour in range(24):
            if hour not in hourly_distribution:
                hourly_distribution[hour] = 0
        
        conn.close()
        
        return {
            'daily_usage': daily_usage,
            'totals': totals,
            'top_api_keys': top_api_keys,
            'top_domains': top_domains,
            'hourly_distribution': hourly_distribution,
            'date_range': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'view_type': view_type
        }
        
    except Exception as e:
        conn.close()
        raise Exception(f"Analytics query error: {str(e)}")

def get_usage_summary():
    """Get quick summary statistics"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # Get today's usage
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT SUM(count) as today_requests
            FROM usage_day 
            WHERE day_key = ?
        ''', (today,))
        
        today_requests = cursor.fetchone()[0] or 0
        
        # Get yesterday's usage
        yesterday = (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT SUM(count) as yesterday_requests
            FROM usage_day 
            WHERE day_key = ?
        ''', (yesterday,))
        
        yesterday_requests = cursor.fetchone()[0] or 0
        
        # Get this month's usage
        this_month = datetime.now().strftime('%Y-%m')
        cursor.execute('''
            SELECT SUM(count) as month_requests
            FROM usage_month 
            WHERE month_key = ?
        ''', (this_month,))
        
        month_requests = cursor.fetchone()[0] or 0
        
        # Get total active API keys
        cursor.execute('SELECT COUNT(*) FROM api_keys WHERE is_active = 1')
        active_api_keys = cursor.fetchone()[0]
        
        # Get total active domains
        cursor.execute('SELECT COUNT(*) FROM authorized_domains WHERE is_active = 1')
        active_domains = cursor.fetchone()[0]
        
        # Get average daily requests (last 7 days)
        seven_days_ago = (datetime.now().date() - timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT AVG(daily_total) as avg_daily
            FROM (
                SELECT day_key, SUM(count) as daily_total
                FROM usage_day
                WHERE day_key >= ?
                GROUP BY day_key
            )
        ''', (seven_days_ago,))
        
        avg_daily = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'today_requests': today_requests,
            'yesterday_requests': yesterday_requests,
            'month_requests': month_requests,
            'active_api_keys': active_api_keys,
            'active_domains': active_domains,
            'avg_daily_requests': round(avg_daily, 1)
        }
        
    except Exception as e:
        conn.close()
        raise Exception(f"Summary query error: {str(e)}")

def get_rate_limit_violations():
    """Get recent rate limit violations for monitoring"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # Get API keys that hit limits recently
        yesterday = (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT ak.name, ak.per_minute_limit, ak.per_day_limit, ak.per_month_limit,
                   MAX(ud.count) as max_daily_usage
            FROM api_keys ak
            LEFT JOIN usage_day ud ON ak.key_hash = ud.identifier AND ud.day_key >= ?
            WHERE ak.is_active = 1
            GROUP BY ak.key_hash, ak.name, ak.per_minute_limit, ak.per_day_limit, ak.per_month_limit
            HAVING max_daily_usage >= ak.per_day_limit * 0.8
            ORDER BY max_daily_usage DESC
        ''', (yesterday,))
        
        api_key_violations = []
        for row in cursor.fetchall():
            name, per_min, per_day, per_month, max_usage = row
            violation_percentage = (max_usage / per_day * 100) if per_day > 0 else 0
            api_key_violations.append({
                'name': name,
                'max_usage': max_usage or 0,
                'daily_limit': per_day,
                'violation_percentage': round(violation_percentage, 1)
            })
        
        # Get domains that hit limits recently
        cursor.execute('''
            SELECT ad.domain, ad.per_minute_limit, ad.per_day_limit, ad.per_month_limit,
                   MAX(ud.count) as max_daily_usage
            FROM authorized_domains ad
            LEFT JOIN usage_day ud ON ad.domain = ud.identifier AND ud.day_key >= ?
            WHERE ad.is_active = 1
            GROUP BY ad.domain, ad.per_minute_limit, ad.per_day_limit, ad.per_month_limit
            HAVING max_daily_usage >= ad.per_day_limit * 0.8
            ORDER BY max_daily_usage DESC
        ''', (yesterday,))
        
        domain_violations = []
        for row in cursor.fetchall():
            domain, per_min, per_day, per_month, max_usage = row
            violation_percentage = (max_usage / per_day * 100) if per_day > 0 else 0
            domain_violations.append({
                'domain': domain,
                'max_usage': max_usage or 0,
                'daily_limit': per_day,
                'violation_percentage': round(violation_percentage, 1)
            })
        
        conn.close()
        
        return {
            'api_key_violations': api_key_violations,
            'domain_violations': domain_violations
        }
        
    except Exception as e:
        conn.close()
        raise Exception(f"Violations query error: {str(e)}")

# V1 Admin API Enhanced Database Functions - Scalable for large datasets
# Note: add_database_indexes() function is defined earlier and called during startup

def get_api_keys_v1(page: int = 1, page_size: int = 25, search: str = "", 
                   sort_by: APIKeySortField = APIKeySortField.created_at, sort_order: SortOrder = SortOrder.desc,
                   is_active: Optional[bool] = None, created_after: Optional[datetime] = None, created_before: Optional[datetime] = None):
    """Enhanced API keys retrieval with full filtering, sorting, and pagination"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    # Build WHERE clause dynamically
    where_conditions = []
    params = []
    
    # Search functionality
    if search:
        search_pattern = f'%{search}%'
        where_conditions.append('(name LIKE ? OR description LIKE ?)')
        params.extend([search_pattern, search_pattern])
    
    # Status filter
    if is_active is not None:
        where_conditions.append('is_active = ?')
        params.append(is_active)
    
    # Date filters (now properly validated)
    if created_after:
        where_conditions.append('created_at >= ?')
        params.append(created_after.isoformat())
    if created_before:
        where_conditions.append('created_at <= ?')
        params.append(created_before.isoformat())
    
    where_clause = 'WHERE ' + ' AND '.join(where_conditions) if where_conditions else ''
    
    # Use secure enum values - no longer vulnerable to SQL injection
    order_clause = f'ORDER BY {sort_by.value} {sort_order.value.upper()}'
    
    # Get total count
    count_query = f'SELECT COUNT(*) FROM api_keys {where_clause}'
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Calculate pagination
    offset = (page - 1) * page_size
    total_pages = (total + page_size - 1) // page_size
    
    # Get paginated results
    query = f'''
        SELECT id, key_hash, name, description, per_minute_limit, per_day_limit, per_month_limit, 
               is_active, created_at, updated_at
        FROM api_keys 
        {where_clause}
        {order_clause}
        LIMIT ? OFFSET ?
    '''
    cursor.execute(query, params + [page_size, offset])
    
    items = []
    for row in cursor.fetchall():
        items.append({
            'id': row[0],
            'key_hash': row[1],
            'name': row[2],
            'description': row[3],
            'per_minute_limit': row[4],
            'per_day_limit': row[5],
            'per_month_limit': row[6],
            'is_active': bool(row[7]),
            'created_at': row[8],
            'updated_at': row[9]
        })
    
    conn.close()
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }

def get_domains_v1(page: int = 1, page_size: int = 25, search: str = "", 
                  sort_by: DomainSortField = DomainSortField.created_at, sort_order: SortOrder = SortOrder.desc,
                  is_active: Optional[bool] = None, created_after: Optional[datetime] = None, created_before: Optional[datetime] = None):
    """Enhanced domains retrieval with full filtering, sorting, and pagination"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    # Build WHERE clause dynamically
    where_conditions = []
    params = []
    
    # Search functionality
    if search:
        search_pattern = f'%{search}%'
        where_conditions.append('domain LIKE ?')
        params.append(search_pattern)
    
    # Status filter
    if is_active is not None:
        where_conditions.append('is_active = ?')
        params.append(is_active)
    
    # Date filters (now properly validated)
    if created_after:
        where_conditions.append('created_at >= ?')
        params.append(created_after.isoformat())
    if created_before:
        where_conditions.append('created_at <= ?')
        params.append(created_before.isoformat())
    
    where_clause = 'WHERE ' + ' AND '.join(where_conditions) if where_conditions else ''
    
    # Use secure enum values - no longer vulnerable to SQL injection
    order_clause = f'ORDER BY {sort_by.value} {sort_order.value.upper()}'
    
    # Get total count
    count_query = f'SELECT COUNT(*) FROM authorized_domains {where_clause}'
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Calculate pagination
    offset = (page - 1) * page_size
    total_pages = (total + page_size - 1) // page_size
    
    # Get paginated results
    query = f'''
        SELECT id, domain, per_minute_limit, per_day_limit, per_month_limit, 
               is_active, created_at, updated_at
        FROM authorized_domains 
        {where_clause}
        {order_clause}
        LIMIT ? OFFSET ?
    '''
    cursor.execute(query, params + [page_size, offset])
    
    items = []
    for row in cursor.fetchall():
        items.append({
            'id': row[0],
            'domain': row[1],
            'per_minute_limit': row[2],
            'per_day_limit': row[3],
            'per_month_limit': row[4],
            'is_active': bool(row[5]),
            'created_at': row[6],
            'updated_at': row[7]
        })
    
    conn.close()
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }

def bulk_update_api_keys(bulk_op: BulkOperation):
    """Perform bulk operations on API keys with secure validation"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    operation = bulk_op.operation.value  # Initialize early to avoid unbound error
    try:
        ids = bulk_op.ids
        payload = bulk_op.payload
        
        # Generate secure placeholders for parameterized queries
        placeholders = ','.join(['?'] * len(ids))
        
        if operation == "delete":
            cursor.execute(f'DELETE FROM api_keys WHERE id IN ({placeholders})', ids)
        elif operation == "activate":
            cursor.execute(f'UPDATE api_keys SET is_active = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id IN ({placeholders})', ids)
        elif operation == "deactivate":
            cursor.execute(f'UPDATE api_keys SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP WHERE id IN ({placeholders})', ids)
        elif operation == "update_limits" and payload is not None:
            # Payload is already validated by Pydantic model
            params = []
            set_clause = []
            
            if payload.per_minute_limit is not None:
                params.append(payload.per_minute_limit)
                set_clause.append('per_minute_limit = ?')
            if payload.per_day_limit is not None:
                params.append(payload.per_day_limit)
                set_clause.append('per_day_limit = ?')
            if payload.per_month_limit is not None:
                params.append(payload.per_month_limit)
                set_clause.append('per_month_limit = ?')
            
            if set_clause:
                set_clause.append('updated_at = CURRENT_TIMESTAMP')
                params.extend(ids)
                cursor.execute(f'UPDATE api_keys SET {", ".join(set_clause)} WHERE id IN ({placeholders})', params)
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        return {"success": True, "affected_rows": affected_rows, "operation": operation}
    
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"success": False, "error": str(e), "operation": operation}

def bulk_update_domains(bulk_op: BulkOperation):
    """Perform bulk operations on domains with secure validation"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    operation = bulk_op.operation.value  # Initialize early to avoid unbound error
    try:
        ids = bulk_op.ids
        payload = bulk_op.payload
        
        # Generate secure placeholders for parameterized queries
        placeholders = ','.join(['?'] * len(ids))
        
        if operation == "delete":
            cursor.execute(f'DELETE FROM authorized_domains WHERE id IN ({placeholders})', ids)
        elif operation == "activate":
            cursor.execute(f'UPDATE authorized_domains SET is_active = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id IN ({placeholders})', ids)
        elif operation == "deactivate":
            cursor.execute(f'UPDATE authorized_domains SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP WHERE id IN ({placeholders})', ids)
        elif operation == "update_limits" and payload is not None:
            # Payload is already validated by Pydantic model
            params = []
            set_clause = []
            
            if payload.per_minute_limit is not None:
                params.append(payload.per_minute_limit)
                set_clause.append('per_minute_limit = ?')
            if payload.per_day_limit is not None:
                params.append(payload.per_day_limit)
                set_clause.append('per_day_limit = ?')
            if payload.per_month_limit is not None:
                params.append(payload.per_month_limit)
                set_clause.append('per_month_limit = ?')
            
            if set_clause:
                set_clause.append('updated_at = CURRENT_TIMESTAMP')
                params.extend(ids)
                cursor.execute(f'UPDATE authorized_domains SET {", ".join(set_clause)} WHERE id IN ({placeholders})', params)
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        return {"success": True, "affected_rows": affected_rows, "operation": operation}
    
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"success": False, "error": str(e), "operation": operation}

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key if provided"""
    if credentials:
        api_key = credentials.credentials
        # Hash the provided API key to check against database
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Check if the key exists in the database
        conn = sqlite3.connect('astrology_db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT key_hash FROM api_keys WHERE key_hash = ? AND is_active = 1', (key_hash,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return api_key
    return None

def cleanup_expired_sessions():
    """Remove expired sessions"""
    now = datetime.now()
    expired_tokens = []
    
    for token, session_data in ACTIVE_SESSIONS.items():
        session_age = (now - session_data['created_at']).total_seconds()
        if session_age > SESSION_TIMEOUT:
            expired_tokens.append(token)
    
    for token in expired_tokens:
        del ACTIVE_SESSIONS[token]
    
    return len(expired_tokens)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using bcrypt"""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def check_domain_authorization(request: Request):
    """Check if request comes from authorized domain with stricter validation"""
    # Clean up any expired sessions first
    cleanup_expired_sessions()
    
    host = request.headers.get('host', '').split(':')[0].lower()
    origin = request.headers.get('origin', '')
    referer = request.headers.get('referer', '')
    
    # Get all authorized domains (both in-memory and database)
    all_authorized_domains = set(AUTHORIZED_DOMAINS)  # Start with in-memory domains
    db_domains = get_authorized_domains()  # Get domains from database
    for db_domain in db_domains:
        all_authorized_domains.add(db_domain['domain'])
    
    # Check direct host with exact match
    if host in all_authorized_domains:
        return True
    
    # Check if host ends with any authorized domain (for subdomains)
    for domain in all_authorized_domains:
        if host.endswith('.' + domain) or host == domain:
            return True
    
    # Check origin with stricter validation
    if origin:
        try:
            from urllib.parse import urlparse
            origin_host = urlparse(origin).hostname
            if origin_host and origin_host.lower() in all_authorized_domains:
                return True
            # Check subdomains for origin
            for domain in all_authorized_domains:
                if origin_host and (origin_host.endswith('.' + domain) or origin_host == domain):
                    return True
        except Exception:
            pass
    
    # Check referer with stricter validation
    if referer:
        try:
            from urllib.parse import urlparse
            referer_host = urlparse(referer).hostname
            if referer_host and referer_host.lower() in all_authorized_domains:
                return True
            # Check subdomains for referer
            for domain in all_authorized_domains:
                if referer_host and (referer_host.endswith('.' + domain) or referer_host == domain):
                    return True
        except Exception:
            pass
    
    return False

def verify_access(request: Request, api_key: str = Depends(verify_api_key)):
    """Verify API key - secure authentication required for all API access"""
    # API key is required for all access - no spoofable domain authorization
    if not api_key:
        raise HTTPException(status_code=403, detail="Access denied. Valid API key required.")
    
    # Hash the API key to match database storage
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    # Get API key limits from database using hash
    key_limits = get_api_key_limits(key_hash)
    if not key_limits:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    if not key_limits['is_active']:
        raise HTTPException(status_code=403, detail="API key is disabled")
    
    # Check and increment rate limits using the hash for identification
    success, message = check_and_increment_usage(
        key_hash, 'api_key',
        key_limits['per_minute_limit'],
        key_limits['per_day_limit'], 
        key_limits['per_month_limit']
    )
    
    if not success:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {message}")
    
    return True

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main frontend interface"""
    try:
        with open('static/index.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Vedic Astrology Calculator</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <h1>Vedic Astrology Calculator</h1>
            <p>Welcome to the Vedic Astrology Calculator API</p>
            <p>Available endpoints:</p>
            <ul>
                <li><a href="/chart">/chart</a> - Calculate chart (GET/POST)</li>
                <li><a href="/admin">/admin</a> - Admin panel</li>
                <li><a href="/health">/health</a> - Health check</li>
            </ul>
        </body>
        </html>
        """

@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    """Serve the admin login page"""
    try:
        with open('static/admin.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Panel - Vedic Astrology Calculator</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .login-form { max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                input, button { width: 100%; padding: 10px; margin: 5px 0; box-sizing: border-box; }
                button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                button:hover { background-color: #45a049; }
                .error { color: red; }
                .success { color: green; }
                .admin-panel { display: none; }
                .section { margin: 20px 0; padding: 15px; border: 1px solid #eee; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="login-form" id="loginForm">
                <h2>Admin Login</h2>
                <form onsubmit="adminLogin(event)">
                    <input type="text" id="username" placeholder="Username" required>
                    <input type="password" id="password" placeholder="Password" required>
                    <button type="submit">Login</button>
                </form>
                <div id="loginMessage"></div>
            </div>
            
            <div class="admin-panel" id="adminPanel">
                <h1>Admin Panel</h1>
                
                <div class="section">
                    <h3>API Keys</h3>
                    <form onsubmit="createApiKey(event)">
                        <input type="text" id="keyName" placeholder="API Key Name" required>
                        <input type="text" id="keyDesc" placeholder="Description (optional)">
                        <button type="submit">Create API Key</button>
                    </form>
                    <div id="apiKeysList"></div>
                </div>
                
                <div class="section">
                    <h3>Authorized Domains</h3>
                    <form onsubmit="addDomain(event)">
                        <input type="text" id="domainName" placeholder="Domain (e.g., example.com)" required>
                        <button type="submit">Add Domain</button>
                    </form>
                    <div id="domainsList"></div>
                </div>
                
                <div class="section">
                    <h3>Change Password</h3>
                    <form onsubmit="changePassword(event)">
                        <input type="password" id="currentPassword" placeholder="Current Password" required>
                        <input type="password" id="newPassword" placeholder="New Password (min 8 chars, 1 digit, 1 uppercase)" required>
                        <input type="password" id="confirmPassword" placeholder="Confirm New Password" required>
                        <button type="submit">Change Password</button>
                    </form>
                    <div id="passwordChangeMessage"></div>
                </div>
                
                <button onclick="logout()">Logout</button>
            </div>
            
            <script>
                let sessionToken = localStorage.getItem('adminToken');
                
                function handleSessionExpiry() {
                    // Clear expired token and show login form
                    localStorage.removeItem('adminToken');
                    sessionToken = null;
                    showLoginForm();
                    alert('Your session has expired. Please login again.');
                }
                
                function showLoginForm() {
                    document.getElementById('loginForm').style.display = 'block';
                    document.getElementById('adminPanel').style.display = 'none';
                }
                
                if (sessionToken) {
                    showAdminPanel();
                }
                
                async function adminLogin(event) {
                    event.preventDefault();
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;
                    
                    try {
                        const response = await fetch('/admin/login', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ username, password })
                        });
                        
                        const data = await response.json();
                        
                        if (response.ok) {
                            sessionToken = data.token;
                            localStorage.setItem('adminToken', sessionToken);
                            showAdminPanel();
                        } else {
                            document.getElementById('loginMessage').innerHTML = '<div class="error">' + data.detail + '</div>';
                        }
                    } catch (error) {
                        document.getElementById('loginMessage').innerHTML = '<div class="error">Login failed</div>';
                    }
                }
                
                function showAdminPanel() {
                    document.getElementById('loginForm').style.display = 'none';
                    document.getElementById('adminPanel').style.display = 'block';
                    loadApiKeys();
                    loadDomains();
                }
                
                async function loadApiKeys() {
                    try {
                        const response = await fetch('/admin/api-keys', {
                            headers: { 'Authorization': 'Bearer ' + sessionToken }
                        });
                        
                        if (response.status === 401 || response.status === 403) {
                            handleSessionExpiry();
                            return;
                        }
                        
                        const data = await response.json();
                        
                        let html = '<h4>Existing API Keys:</h4>';
                        for (let key in data.api_keys) {
                            html += '<div>' + data.api_keys[key].name + ' - ' + key + ' <button onclick="deleteApiKey(\'' + key + '\')" style="background-color: #f44336;">Delete</button></div>';
                        }
                        document.getElementById('apiKeysList').innerHTML = html;
                    } catch (error) {
                        console.error('Failed to load API keys');
                    }
                }
                
                async function loadDomains() {
                    try {
                        const response = await fetch('/admin/domains', {
                            headers: { 'Authorization': 'Bearer ' + sessionToken }
                        });
                        
                        if (response.status === 401 || response.status === 403) {
                            handleSessionExpiry();
                            return;
                        }
                        
                        const data = await response.json();
                        
                        let html = '<h4>Authorized Domains:</h4>';
                        data.domains.forEach(domain => {
                            html += '<div>' + domain + ' <button onclick="deleteDomain(\'' + domain + '\')" style="background-color: #f44336;">Delete</button></div>';
                        });
                        document.getElementById('domainsList').innerHTML = html;
                    } catch (error) {
                        console.error('Failed to load domains');
                    }
                }
                
                async function createApiKey(event) {
                    event.preventDefault();
                    const name = document.getElementById('keyName').value;
                    const description = document.getElementById('keyDesc').value;
                    
                    try {
                        const response = await fetch('/admin/api-keys', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + sessionToken
                            },
                            body: JSON.stringify({ name, description })
                        });
                        
                        if (response.status === 401 || response.status === 403) {
                            handleSessionExpiry();
                            return;
                        }
                        
                        if (response.ok) {
                            document.getElementById('keyName').value = '';
                            document.getElementById('keyDesc').value = '';
                            loadApiKeys();
                        }
                    } catch (error) {
                        console.error('Failed to create API key');
                    }
                }
                
                async function addDomain(event) {
                    event.preventDefault();
                    const domain = document.getElementById('domainName').value;
                    
                    try {
                        const response = await fetch('/admin/domains', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + sessionToken
                            },
                            body: JSON.stringify({ domain })
                        });
                        
                        if (response.status === 401 || response.status === 403) {
                            handleSessionExpiry();
                            return;
                        }
                        
                        if (response.ok) {
                            document.getElementById('domainName').value = '';
                            loadDomains();
                        }
                    } catch (error) {
                        console.error('Failed to add domain');
                    }
                }
                
                async function deleteApiKey(key) {
                    if (confirm('Delete this API key?')) {
                        try {
                            const response = await fetch('/admin/api-keys/' + key, {
                                method: 'DELETE',
                                headers: { 'Authorization': 'Bearer ' + sessionToken }
                            });
                            
                            if (response.status === 401 || response.status === 403) {
                                handleSessionExpiry();
                                return;
                            }
                            
                            loadApiKeys();
                        } catch (error) {
                            console.error('Failed to delete API key');
                        }
                    }
                }
                
                async function deleteDomain(domain) {
                    if (confirm('Remove this domain?')) {
                        try {
                            const response = await fetch('/admin/domains/' + domain, {
                                method: 'DELETE',
                                headers: { 'Authorization': 'Bearer ' + sessionToken }
                            });
                            
                            if (response.status === 401 || response.status === 403) {
                                handleSessionExpiry();
                                return;
                            }
                            
                            loadDomains();
                        } catch (error) {
                            console.error('Failed to delete domain');
                        }
                    }
                }
                
                async function changePassword(event) {
                    event.preventDefault();
                    const currentPassword = document.getElementById('currentPassword').value;
                    const newPassword = document.getElementById('newPassword').value;
                    const confirmPassword = document.getElementById('confirmPassword').value;
                    
                    // Validate passwords match
                    if (newPassword !== confirmPassword) {
                        document.getElementById('passwordChangeMessage').innerHTML = '<div class="error">New passwords do not match</div>';
                        return;
                    }
                    
                    try {
                        const response = await fetch('/admin/password-change', {
                            method: 'POST',
                            headers: { 
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + sessionToken
                            },
                            body: JSON.stringify({ 
                                current_password: currentPassword, 
                                new_password: newPassword 
                            })
                        });
                        
                        if (response.status === 401 || response.status === 403) {
                            handleSessionExpiry();
                            return;
                        }
                        
                        const data = await response.json();
                        
                        if (response.ok) {
                            document.getElementById('passwordChangeMessage').innerHTML = '<div class="success">' + data.message + '</div>';
                            document.getElementById('currentPassword').value = '';
                            document.getElementById('newPassword').value = '';
                            document.getElementById('confirmPassword').value = '';
                        } else {
                            document.getElementById('passwordChangeMessage').innerHTML = '<div class="error">' + data.detail + '</div>';
                        }
                    } catch (error) {
                        document.getElementById('passwordChangeMessage').innerHTML = '<div class="error">Failed to change password</div>';
                    }
                }
                
                function logout() {
                    localStorage.removeItem('adminToken');
                    location.reload();
                }
            </script>
        </body>
        </html>
        """

@app.get("/chart")
async def calculate_chart_get(
    request: Request,
    year: int,
    month: int, 
    day: int,
    hour: int,
    lat: float,
    lon: float,
    minute: int = 0,
    second: int = 0,
    tz: str = 'UTC',
    ayanamsha: str = 'lahiri',
    house_system: str = 'placidus',
    natal_ayanamsha: str = '',
    natal_house_system: str = '',
    transit_ayanamsha: str = '',
    transit_house_system: str = '',
    _: bool = Depends(verify_access)
):
    """GET endpoint for chart calculation with natal and transit data"""
    # Use specific parameters if provided, otherwise fall back to general ones
    natal_ayan = natal_ayanamsha if natal_ayanamsha else ayanamsha
    natal_house = natal_house_system if natal_house_system else house_system
    transit_ayan = transit_ayanamsha if transit_ayanamsha else ayanamsha
    transit_house = transit_house_system if transit_house_system else house_system
    
    result = await build_natal_transit_response(
        year, month, day, hour, minute, second,
        lat, lon, tz, natal_ayan, natal_house, transit_ayan, transit_house
    )
    return JSONResponse(content=result)

@app.post("/chart")
async def calculate_chart_post(
    request: Request,
    chart_data: ChartRequest,
    _: bool = Depends(verify_access)
):
    """POST endpoint for chart calculation with natal and transit data"""
    # Use specific parameters if provided, otherwise fall back to general ones
    natal_ayan = chart_data.natal_ayanamsha if chart_data.natal_ayanamsha else chart_data.ayanamsha
    natal_house = chart_data.natal_house_system if chart_data.natal_house_system else chart_data.house_system
    transit_ayan = chart_data.transit_ayanamsha if chart_data.transit_ayanamsha else chart_data.ayanamsha
    transit_house = chart_data.transit_house_system if chart_data.transit_house_system else chart_data.house_system
    
    result = await build_natal_transit_response(
        chart_data.year, chart_data.month, chart_data.day, 
        chart_data.hour, chart_data.minute, chart_data.second,
        chart_data.lat, chart_data.lon, 
        chart_data.tz, natal_ayan, natal_house, transit_ayan, transit_house
    )
    return JSONResponse(content=result)

async def calculate_chart_internal(
    year: int,
    month: int, 
    day: int,
    hour: int,
    minute: int,
    second: int,
    lat: float,
    lon: float,
    tz: str = 'UTC',
    ayanamsha: str = 'lahiri',
    house_system: str = 'placidus'
):
    """
    Calculate Vedic astrology chart with planetary longitudes and Ascendant.
    
    Parameters:
    - year: Year (e.g., 2024)
    - month: Month (1-12)
    - day: Day (1-31)
    - hour: Hour in UT decimal format (e.g., 15.5 for 3:30 PM)
    - lat: Latitude in degrees (positive for North)
    - lon: Longitude in degrees (positive for East)
    
    Returns JSON with julian_day_ut, ascendant_deg, and planets_deg dictionary.
    """
    try:
        # Validate inputs
        if not (1 <= month <= 12):
            raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
        if not (1 <= day <= 31):
            raise HTTPException(status_code=400, detail="Day must be between 1 and 31")
        if not (0 <= hour <= 23):
            raise HTTPException(status_code=400, detail="Hour must be between 0 and 23")
        if not (0 <= minute <= 59):
            raise HTTPException(status_code=400, detail="Minute must be between 0 and 59")
        if not (0 <= second <= 59):
            raise HTTPException(status_code=400, detail="Second must be between 0 and 59")
        if not (-90 <= lat <= 90):
            raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90 degrees")
        if not (-180 <= lon <= 180):
            raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180 degrees")
        
        # Validate ayanamsha
        if ayanamsha not in AYANAMSHA_OPTIONS:
            raise HTTPException(status_code=400, detail=f"Invalid ayanamsha. Must be one of: {list(AYANAMSHA_OPTIONS.keys())}")
        
        # Validate house system
        if house_system not in HOUSE_SYSTEMS:
            raise HTTPException(status_code=400, detail=f"Invalid house system. Must be one of: {list(HOUSE_SYSTEMS.keys())}")
        
        # Convert local time to UT using timezone
        hour_ut = convert_timezone_to_ut(year, month, day, hour, minute, second, tz)
        
        # Convert to Julian Day using UT time
        julian_day_ut = swe.julday(year, month, day, hour_ut)
        
        # Set the ayanamsha
        ayanamsha_info = AYANAMSHA_OPTIONS[ayanamsha]
        swe.set_sid_mode(ayanamsha_info['id'])
        
        # Get ayanamsha value for the given date
        ayanamsha_value = swe.get_ayanamsa_ut(julian_day_ut)
        
        # Calculate houses and Ascendant using selected house system in sidereal mode
        # Using sidereal flag for Vedic astrology  
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
        house_system_code = HOUSE_SYSTEMS[house_system].encode('ascii')
        houses, ascmc = swe.houses_ex(julian_day_ut, lat, lon, house_system_code, flags)
        ascendant_deg = round(ascmc[0], 2)  # Ascendant is the first element in ascmc
        
        # Prepare house cusps with full precision
        house_cusps = [round(house, 6) for house in houses[:12]]  # Only need first 12 houses
        
        # Calculate planetary positions with full precision
        planets_deg = {}
        planets_full_precision = {}
        
        for planet_name, planet_id in PLANETS.items():
            try:
                # Calculate sidereal position using explicit Swiss Ephemeris and sidereal flags
                flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
                position, retflag = swe.calc_ut(julian_day_ut, planet_id, flags)
                longitude = position[0]  # Longitude is the first element
                planets_deg[planet_name] = round(longitude, 2)
                planets_full_precision[planet_name] = round(longitude, 6)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error calculating {planet_name}: {str(e)}")
        
        # Calculate Ketu (Rahu + 180 degrees)
        rahu_longitude = planets_full_precision['Rahu']
        ketu_longitude = (rahu_longitude + 180) % 360
        planets_deg['Ketu'] = round(ketu_longitude, 2)
        planets_full_precision['Ketu'] = round(ketu_longitude, 6)
        
        # Prepare enhanced response with all frontend-expected fields
        ascendant_full_precision = round(ascmc[0], 6)
        
        return JSONResponse(content={
            "julian_day_ut": round(julian_day_ut, 6),
            "ascendant_deg": ascendant_deg,
            "ascendant_full_precision": ascendant_full_precision,
            "planets_deg": planets_deg,
            "planets_full_precision": planets_full_precision,
            "house_cusps": house_cusps,
            "house_system_used": HOUSE_SYSTEM_NAMES[house_system],
            "ayanamsha_name": ayanamsha_info['name'],
            "ayanamsha_value_decimal": round(ayanamsha_value, 6),
            "ayanamsha_value_dms": decimal_to_dms(ayanamsha_value),
            "timezone_used": tz,
            "input_time_ut": round(hour_ut, 6)
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def build_natal_transit_response(
    year: int, month: int, day: int, hour: int, minute: int, second: int,
    lat: float, lon: float, tz: str, natal_ayanamsha: str, natal_house_system: str,
    transit_ayanamsha: str, transit_house_system: str
):
    """Build combined natal and transit response"""
    try:
        # Calculate natal chart with natal-specific ayanamsha and house system
        natal_result = await calculate_chart_internal(
            year, month, day, hour, minute, second,
            lat, lon, tz, natal_ayanamsha, natal_house_system
        )
        
        # Extract natal data from JSONResponse
        natal_data = json.loads(bytes(natal_result.body).decode())
        
        # Get current date and time for transit chart in user's timezone
        user_tz = pytz.timezone(tz)
        now_utc = datetime.now(pytz.UTC)
        now_local = now_utc.astimezone(user_tz)
        
        # Calculate transit chart with transit-specific ayanamsha and house system
        transit_result = await calculate_chart_internal(
            now_local.year, now_local.month, now_local.day,
            now_local.hour, now_local.minute, now_local.second,
            lat, lon, tz, transit_ayanamsha, transit_house_system
        )
        
        # Extract transit data from JSONResponse
        transit_data = json.loads(bytes(transit_result.body).decode())
        
        # Structure the clean response with only fields used by frontend
        response_data = {
            # Frontend display data
            "other_details": {
                "natal_date_formatted": convert_julian_to_date(natal_data["julian_day_ut"], tz),
                "transit_date_formatted": convert_julian_to_date(transit_data["julian_day_ut"], tz),
                "natal_ayanamsha_name": natal_data["ayanamsha_name"],
                "transit_ayanamsha_name": transit_data["ayanamsha_name"],
                "ayanamsha_value_natal": natal_data["ayanamsha_value_decimal"],
                "ayanamsha_value_transit": transit_data["ayanamsha_value_decimal"],
                "natal_house_system_used": natal_data["house_system_used"],
                "transit_house_system_used": transit_data["house_system_used"],
                "timezone_used": natal_data["timezone_used"],
                "natal_input_time_ut": natal_data["input_time_ut"],
                "transit_input_time_ut": natal_data["input_time_ut"]  # Use same as natal per user request
            },
            
            "natal_planets": dict(Ascendant=natal_data["ascendant_full_precision"], **natal_data["planets_full_precision"]),
            "natal_house_cusps": {f"House {i + 1}": cusp for i, cusp in enumerate(natal_data["house_cusps"])},
            "transit_planets": dict(Ascendant=transit_data["ascendant_full_precision"], **transit_data["planets_full_precision"]),
            "transit_house_cusps": {f"House {i + 1}": cusp for i, cusp in enumerate(transit_data["house_cusps"])}
        }
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating natal-transit charts: {str(e)}")

def verify_admin_session(request: Request):
    """Verify admin session token with timeout validation"""
    # Clean up expired sessions
    cleanup_expired_sessions()
    
    auth_header = request.headers.get('authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = auth_header.split(' ')[1]
    if token not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    session_data = ACTIVE_SESSIONS[token]
    now = datetime.now()
    
    # Check session timeout
    session_age = (now - session_data['created_at']).total_seconds()
    if session_age > SESSION_TIMEOUT:
        del ACTIVE_SESSIONS[token]
        raise HTTPException(status_code=401, detail="Session expired")
    
    # Update last activity
    session_data['last_activity'] = now
    
    return session_data['username']

# Admin endpoints
@app.post("/admin/login")
async def admin_login(login_data: AdminLogin):
    """Secure admin login endpoint with bcrypt password verification using database"""
    # Clean up expired sessions first
    cleanup_expired_sessions()
    
    # Rate limiting: simple check to prevent brute force (in production, use proper rate limiting)
    if len(ACTIVE_SESSIONS) > 10:
        raise HTTPException(status_code=429, detail="Too many active sessions. Try again later.")
    
    # Get admin from database
    admin_user = get_admin_by_username(login_data.username)
    if admin_user and verify_password(login_data.password, admin_user['password_hash']):
        # Check if password change is required
        must_change_password = admin_user.get('must_change_password', False)
        
        # Generate secure session token
        token = secrets.token_urlsafe(32)
        ACTIVE_SESSIONS[token] = {
            'username': login_data.username,
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'password_change_required': must_change_password
        }
        
        response = {
            "token": token, 
            "message": "Login successful",
            "expires_in": SESSION_TIMEOUT,
            "password_change_required": must_change_password
        }
        
        if must_change_password:
            response["message"] = "Login successful - Password change required"
            response["warning"] = "You must change your password before accessing admin functions"
        
        return response
    else:
        # Add a small delay to prevent timing attacks
        import time
        time.sleep(0.5)
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/admin/password-change")
async def admin_password_change(password_data: PasswordChangeRequest, username: str = Depends(verify_admin_session)):
    """Change admin password with current password verification"""
    current_password = password_data.current_password
    new_password = password_data.new_password
    
    # Validate new password strength
    if len(new_password) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters long")
    
    if not any(c.isdigit() for c in new_password):
        raise HTTPException(status_code=400, detail="New password must contain at least one digit")
    
    if not any(c.isupper() for c in new_password):
        raise HTTPException(status_code=400, detail="New password must contain at least one uppercase letter")
    
    # Get current admin from database
    admin_user = get_admin_by_username(username)
    if not admin_user:
        raise HTTPException(status_code=401, detail="Admin user not found")
    
    # Verify current password
    if not verify_password(current_password, admin_user['password_hash']):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Generate new password hash
    new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Update password in database and clear change requirement
    if update_admin_password(username, new_password_hash, clear_change_requirement=True):
        # Update active sessions to remove password change requirement
        for token, session_data in ACTIVE_SESSIONS.items():
            if session_data['username'] == username:
                session_data['password_change_required'] = False
        
        return {"message": "Password changed successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update password")

@app.post("/admin/logout")
async def admin_logout(request: Request, admin_user: str = Depends(verify_admin_session)):
    """Secure admin logout endpoint"""
    auth_header = request.headers.get('authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        if token in ACTIVE_SESSIONS:
            del ACTIVE_SESSIONS[token]
    
    return {"message": "Logged out successfully"}

@app.post("/admin/logout-all")
async def admin_logout_all(request: Request, admin_user: str = Depends(verify_admin_session)):
    """Logout from all sessions (emergency logout)"""
    # Keep only the current session or clear all if preferred
    ACTIVE_SESSIONS.clear()
    return {"message": "All sessions terminated successfully"}

@app.get("/admin/api-keys")
async def get_api_keys(request: Request, admin_user: str = Depends(verify_admin_session)):
    """Get all API keys from database with limits"""
    paginated_result = get_api_keys_paginated()
    
    # Convert array format to object format expected by frontend
    api_keys = {}
    for key_info in paginated_result['keys']:
        api_keys[key_info['key_hash']] = {
            'name': key_info['name'],
            'description': key_info['description'],
            'per_minute_limit': key_info['per_minute_limit'],
            'per_day_limit': key_info['per_day_limit'],
            'per_month_limit': key_info['per_month_limit'],
            'is_active': key_info['is_active'],
            'created_at': key_info['created_at'],
            'updated_at': key_info['updated_at']
        }
    
    return {"api_keys": api_keys}

@app.post("/admin/api-keys")
async def create_api_key(request: Request, key_data: CreateAPIKeyRequest, admin_user: str = Depends(verify_admin_session)):
    """Create new API key with rate limits"""
    result = create_api_key_db(
        name=key_data.name,
        description=key_data.description or '',
        per_minute_limit=key_data.per_minute_limit,
        per_day_limit=key_data.per_day_limit,
        per_month_limit=key_data.per_month_limit
    )
    if result:
        return {"api_key": result['api_key'], "message": "API key created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to create API key")

@app.put("/admin/api-keys/{api_key_hash}/limits")
async def update_api_key_limits_endpoint(request: Request, api_key_hash: str, limits_data: UpdateAPIKeyLimitsRequest, admin_user: str = Depends(verify_admin_session)):
    """Update API key rate limits"""
    success = update_api_key_limits(
        key_hash=api_key_hash,
        per_minute_limit=limits_data.per_minute_limit,
        per_day_limit=limits_data.per_day_limit,
        per_month_limit=limits_data.per_month_limit
    )
    if success:
        return {"message": "API key limits updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="API key not found")

@app.delete("/admin/api-keys/{api_key_hash}")
async def delete_api_key(request: Request, api_key_hash: str, admin_user: str = Depends(verify_admin_session)):
    """Delete API key"""
    success = delete_api_key_db(api_key_hash)
    if success:
        return {"message": "API key deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="API key not found")

@app.get("/admin/domains")
async def get_domains(request: Request, admin_user: str = Depends(verify_admin_session)):
    """Get authorized domains with limits from database"""
    domains = get_authorized_domains()
    return {"domains": domains}

@app.post("/admin/domains")
async def add_domain(request: Request, domain_data: CreateDomainRequest, admin_user: str = Depends(verify_admin_session)):
    """Add authorized domain with rate limits"""
    success = add_authorized_domain(
        domain=domain_data.domain,
        per_minute_limit=domain_data.per_minute_limit,
        per_day_limit=domain_data.per_day_limit,
        per_month_limit=domain_data.per_month_limit
    )
    if success:
        return {"message": f"Domain {domain_data.domain} added successfully"}
    else:
        raise HTTPException(status_code=400, detail="Domain already exists or failed to add")

# V1 Admin API Endpoints - Secure and scalable
@app.get("/admin/v1/api-keys", response_model=PaginatedResponse)
async def get_api_keys_v1_endpoint(
    pagination: APIKeyPaginationParams = Depends(),
    filters: APIKeyFilters = Depends(),
    admin_user: str = Depends(verify_admin_session)
):
    """Enhanced API keys retrieval with pagination, search, filtering and sorting"""
    try:
        result = get_api_keys_v1(
            page=pagination.page,
            page_size=pagination.page_size,
            search=pagination.search or "",
            sort_by=pagination.sort_by,
            sort_order=pagination.sort_order,
            is_active=filters.is_active,
            created_after=filters.created_after,
            created_before=filters.created_before
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve API keys: {str(e)}")

@app.post("/admin/v1/api-keys")
async def create_api_key_v1(
    key_data: CreateAPIKeyRequest, 
    admin_user: str = Depends(verify_admin_session)
):
    """Create new API key with enhanced validation"""
    try:
        result = create_api_key_db(
            name=key_data.name,
            description=key_data.description or '',
            per_minute_limit=key_data.per_minute_limit,
            per_day_limit=key_data.per_day_limit,
            per_month_limit=key_data.per_month_limit
        )
        if result:
            return {"api_key": result['api_key'], "message": "API key created successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to create API key")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create API key: {str(e)}")

@app.post("/admin/v1/api-keys/bulk")
async def bulk_api_keys_v1(
    operation: BulkOperation,
    admin_user: str = Depends(verify_admin_session)
):
    """Perform bulk operations on API keys"""
    try:
        result = bulk_update_api_keys(operation)
        if result["success"]:
            return {
                "message": f"Bulk operation completed successfully", 
                "affected_rows": result["affected_rows"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk operation failed: {str(e)}")

@app.get("/admin/v1/domains", response_model=PaginatedResponse)
async def get_domains_v1_endpoint(
    pagination: DomainPaginationParams = Depends(),
    filters: DomainFilters = Depends(),
    admin_user: str = Depends(verify_admin_session)
):
    """Enhanced domains retrieval with pagination, search, filtering and sorting"""
    try:
        result = get_domains_v1(
            page=pagination.page,
            page_size=pagination.page_size,
            search=pagination.search or "",
            sort_by=pagination.sort_by,
            sort_order=pagination.sort_order,
            is_active=filters.is_active,
            created_after=filters.created_after,
            created_before=filters.created_before
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve domains: {str(e)}")

@app.post("/admin/v1/domains")
async def create_domain_v1(
    domain_data: CreateDomainRequest, 
    admin_user: str = Depends(verify_admin_session)
):
    """Create new authorized domain with enhanced validation"""
    try:
        success = add_authorized_domain(
            domain=domain_data.domain,
            per_minute_limit=domain_data.per_minute_limit,
            per_day_limit=domain_data.per_day_limit,
            per_month_limit=domain_data.per_month_limit
        )
        if success:
            return {"message": f"Domain {domain_data.domain} added successfully"}
        else:
            raise HTTPException(status_code=400, detail="Domain already exists or failed to add")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create domain: {str(e)}")

@app.post("/admin/v1/domains/bulk")
async def bulk_domains_v1(
    operation: BulkOperation,
    admin_user: str = Depends(verify_admin_session)
):
    """Perform bulk operations on domains"""
    try:
        result = bulk_update_domains(operation)
        if result["success"]:
            return {
                "message": f"Bulk operation completed successfully", 
                "affected_rows": result["affected_rows"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk operation failed: {str(e)}")

@app.put("/admin/domains/{domain}/limits")
async def update_domain_limits_endpoint(request: Request, domain: str, limits_data: UpdateDomainLimitsRequest, admin_user: str = Depends(verify_admin_session)):
    """Update domain rate limits"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE authorized_domains 
        SET per_minute_limit = ?, per_day_limit = ?, per_month_limit = ?, updated_at = CURRENT_TIMESTAMP
        WHERE domain = ?
    ''', (limits_data.per_minute_limit, limits_data.per_day_limit, limits_data.per_month_limit, domain))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    if success:
        return {"message": f"Domain {domain} limits updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Domain not found")

@app.delete("/admin/domains/{domain}")
async def delete_domain(request: Request, domain: str, admin_user: str = Depends(verify_admin_session)):
    """Remove authorized domain"""
    success = delete_authorized_domain(domain)
    if success:
        return {"message": f"Domain {domain} removed successfully"}
    else:
        raise HTTPException(status_code=404, detail="Domain not found")

# Analytics endpoints
@app.get("/admin/analytics/dashboard")
async def get_analytics_dashboard(
    period: str = "30",
    view_type: str = "all",
    identifier: Optional[str] = None,
    admin_user: str = Depends(verify_admin_session)
):
    """Get comprehensive analytics data for admin dashboard
    
    Args:
        period: Time period - can be 'today', 'yesterday', or number of days (1-365)
        view_type: Filter by 'all', 'api_key', or 'domain'
        identifier: Optional specific API key hash or domain to filter by
    """
    # Handle special periods
    if period == "today":
        days = 1  # This will be overridden by period parameter in get_usage_analytics
    elif period == "yesterday":
        days = 1  # This will be overridden by period parameter in get_usage_analytics 
    else:
        try:
            days = int(period)
            if days < 1 or days > 365:
                raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
        except ValueError:
            raise HTTPException(status_code=400, detail="Period must be 'today', 'yesterday', or a number between 1 and 365")
    
    if view_type not in ["all", "api_key", "domain"]:
        raise HTTPException(status_code=400, detail="view_type must be 'all', 'api_key', or 'domain'")
    
    try:
        analytics = get_usage_analytics(days, view_type, identifier, period)
        summary = get_usage_summary()
        violations = get_rate_limit_violations()
        
        return {
            "analytics": analytics,
            "summary": summary,
            "violations": violations,
            "view_type": view_type,
            "identifier": identifier,
            "period": period,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load analytics: {str(e)}")

@app.get("/admin/analytics/summary")
async def get_analytics_summary(admin_user: str = Depends(verify_admin_session)):
    """Get quick summary statistics for dashboard KPIs"""
    try:
        return get_usage_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load summary: {str(e)}")

@app.get("/admin/analytics/usage/{days}")
async def get_usage_data(days: int, admin_user: str = Depends(verify_admin_session)):
    """Get detailed usage analytics for specified number of days"""
    if days < 1 or days > 365:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
    
    try:
        return get_usage_analytics(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load usage data: {str(e)}")

@app.get("/admin/analytics/violations")
async def get_violations_data(admin_user: str = Depends(verify_admin_session)):
    """Get recent rate limit violations"""
    try:
        return get_rate_limit_violations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load violations: {str(e)}")

@app.get("/admin/analytics/api-keys")
async def get_analytics_api_keys(admin_user: str = Depends(verify_admin_session)):
    """Get list of API keys for analytics dropdown"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT key_hash, name, description, is_active
            FROM api_keys 
            WHERE is_active = 1
            ORDER BY name
        ''')
        
        api_keys = []
        for row in cursor.fetchall():
            key_hash, name, description, is_active = row
            api_keys.append({
                'key_hash': key_hash,
                'name': name,
                'description': description or 'No description',
                'is_active': bool(is_active)
            })
        
        conn.close()
        return {"api_keys": api_keys}
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Failed to load API keys: {str(e)}")

@app.get("/admin/analytics/domains")
async def get_analytics_domains(admin_user: str = Depends(verify_admin_session)):
    """Get list of domains for analytics dropdown"""
    conn = sqlite3.connect('astrology_db.sqlite3')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT domain, description, is_active
            FROM authorized_domains 
            WHERE is_active = 1
            ORDER BY domain
        ''')
        
        domains = []
        for row in cursor.fetchall():
            domain, description, is_active = row
            domains.append({
                'domain': domain,
                'description': description or 'No description',
                'is_active': bool(is_active)
            })
        
        conn.close()
        return {"domains": domains}
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Failed to load domains: {str(e)}")

@app.get("/ayanamsha-options")
async def get_ayanamsha_options():
    """Get available ayanamsha options"""
    return {"options": AYANAMSHA_OPTIONS}

@app.get("/security-status")
async def security_status():
    """Security status endpoint for monitoring"""
    cleanup_expired_sessions()
    return {
        "status": "secure",
        "environment_auth": bool(os.getenv('ADMIN_PASSWORD_HASH')),
        "active_sessions": len(ACTIVE_SESSIONS),
        "authorized_domains": len(AUTHORIZED_DOMAINS),
        "api_keys_count": len(API_KEYS),
        "session_timeout": SESSION_TIMEOUT
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "ephe_path": ephe_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)