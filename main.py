from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import swisseph as swe
import pytz
import os
import json
import secrets
from datetime import datetime
from typing import Dict, Union, Optional
import hashlib

app = FastAPI(title="Vedic Astrology Calculator", description="Calculate planetary longitudes and Ascendant using Swiss Ephemeris")

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

# Simple in-memory storage for admin data
ADMIN_CREDENTIALS = {
    'admin': 'admin123'  # Default admin credentials
}
AUTHORIZED_DOMAINS = set(['localhost', '127.0.0.1', 'replit.dev', 'replit.com'])
API_KEYS = {}
ACTIVE_SESSIONS = {}

# Request models
class ChartRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: float
    lat: float
    lon: float
    tz: str = 'UTC'
    ayanamsha: str = 'lahiri'

class AdminLogin(BaseModel):
    username: str
    password: str

class APIKeyRequest(BaseModel):
    name: str
    description: Optional[str] = ''

class DomainRequest(BaseModel):
    domain: str

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

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key if provided"""
    if credentials:
        if credentials.credentials in API_KEYS:
            return credentials.credentials
    return None

def check_domain_authorization(request: Request):
    """Check if request comes from authorized domain"""
    host = request.headers.get('host', '').split(':')[0]
    origin = request.headers.get('origin', '')
    referer = request.headers.get('referer', '')
    
    # Check direct host
    if host in AUTHORIZED_DOMAINS:
        return True
    
    # Check origin
    if origin:
        try:
            from urllib.parse import urlparse
            origin_host = urlparse(origin).hostname
            if origin_host in AUTHORIZED_DOMAINS:
                return True
        except:
            pass
    
    # Check referer
    if referer:
        try:
            from urllib.parse import urlparse
            referer_host = urlparse(referer).hostname
            if referer_host in AUTHORIZED_DOMAINS:
                return True
        except:
            pass
    
    return False

def verify_access(request: Request, api_key: str = Depends(verify_api_key)):
    """Verify either API key or domain authorization"""
    if api_key:
        return True
    if check_domain_authorization(request):
        return True
    raise HTTPException(status_code=403, detail="Access denied. Valid API key or authorized domain required.")

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
                
                <button onclick="logout()">Logout</button>
            </div>
            
            <script>
                let sessionToken = localStorage.getItem('adminToken');
                
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
                        const data = await response.json();
                        
                        let html = '<h4>Existing API Keys:</h4>';
                        for (let key in data.api_keys) {
                            html += '<div>' + data.api_keys[key].name + ' - ' + key + ' <button onclick="deleteApiKey(\''+key+'\')" style="background-color: #f44336;">Delete</button></div>';
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
                        const data = await response.json();
                        
                        let html = '<h4>Authorized Domains:</h4>';
                        data.domains.forEach(domain => {
                            html += '<div>' + domain + ' <button onclick="deleteDomain(\''+domain+'\')" style="background-color: #f44336;">Delete</button></div>';
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
                            await fetch('/admin/api-keys/' + key, {
                                method: 'DELETE',
                                headers: { 'Authorization': 'Bearer ' + sessionToken }
                            });
                            loadApiKeys();
                        } catch (error) {
                            console.error('Failed to delete API key');
                        }
                    }
                }
                
                async function deleteDomain(domain) {
                    if (confirm('Remove this domain?')) {
                        try {
                            await fetch('/admin/domains/' + domain, {
                                method: 'DELETE',
                                headers: { 'Authorization': 'Bearer ' + sessionToken }
                            });
                            loadDomains();
                        } catch (error) {
                            console.error('Failed to delete domain');
                        }
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
    hour: float,
    lat: float,
    lon: float,
    tz: str = 'UTC',
    ayanamsha: str = 'lahiri',
    _: bool = Depends(verify_access)
):
    """GET endpoint for chart calculation"""
    return await calculate_chart_internal(year, month, day, hour, lat, lon, tz, ayanamsha)

@app.post("/chart")
async def calculate_chart_post(
    request: Request,
    chart_data: ChartRequest,
    _: bool = Depends(verify_access)
):
    """POST endpoint for chart calculation"""
    return await calculate_chart_internal(
        chart_data.year, chart_data.month, chart_data.day, 
        chart_data.hour, chart_data.lat, chart_data.lon, 
        chart_data.tz, chart_data.ayanamsha
    )

async def calculate_chart_internal(
    year: int,
    month: int, 
    day: int,
    hour: float,
    lat: float,
    lon: float,
    tz: str = 'UTC',
    ayanamsha: str = 'lahiri'
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
        if not (0 <= hour < 24):
            raise HTTPException(status_code=400, detail="Hour must be between 0 and 24")
        if not (-90 <= lat <= 90):
            raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90 degrees")
        if not (-180 <= lon <= 180):
            raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180 degrees")
        
        # Convert to Julian Day
        julian_day_ut = swe.julday(year, month, day, hour)
        
        # Calculate houses and Ascendant using Placidus house system in sidereal mode
        # Using sidereal flag for Vedic astrology  
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
        houses, ascmc = swe.houses_ex(julian_day_ut, lat, lon, b'P', flags)
        ascendant_deg = round(ascmc[0], 2)  # Ascendant is the first element in ascmc
        
        # Calculate planetary positions
        planets_deg = {}
        
        for planet_name, planet_id in PLANETS.items():
            try:
                # Calculate sidereal position using explicit Swiss Ephemeris and sidereal flags
                flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
                position, retflag = swe.calc_ut(julian_day_ut, planet_id, flags)
                longitude = position[0]  # Longitude is the first element
                planets_deg[planet_name] = round(longitude, 2)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error calculating {planet_name}: {str(e)}")
        
        # Calculate Ketu (Rahu + 180 degrees)
        rahu_longitude = planets_deg['Rahu']
        ketu_longitude = (rahu_longitude + 180) % 360
        planets_deg['Ketu'] = round(ketu_longitude, 2)
        
        return JSONResponse(content={
            "julian_day_ut": round(julian_day_ut, 6),
            "ascendant_deg": ascendant_deg,
            "planets_deg": planets_deg
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Admin endpoints
@app.post("/admin/login")
async def admin_login(login_data: AdminLogin):
    """Admin login endpoint"""
    if login_data.username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[login_data.username] == login_data.password:
        # Generate session token
        token = secrets.token_urlsafe(32)
        ACTIVE_SESSIONS[token] = login_data.username
        return {"token": token, "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def verify_admin_session(request: Request):
    """Verify admin session token"""
    auth_header = request.headers.get('authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = auth_header.split(' ')[1]
    if token not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return ACTIVE_SESSIONS[token]

@app.get("/admin/api-keys")
async def get_api_keys(request: Request, admin_user: str = Depends(verify_admin_session)):
    """Get all API keys"""
    return {"api_keys": API_KEYS}

@app.post("/admin/api-keys")
async def create_api_key(request: Request, key_data: APIKeyRequest, admin_user: str = Depends(verify_admin_session)):
    """Create new API key"""
    api_key = secrets.token_urlsafe(32)
    API_KEYS[api_key] = {
        "name": key_data.name,
        "description": key_data.description,
        "created_by": admin_user,
        "created_at": datetime.now().isoformat()
    }
    return {"api_key": api_key, "message": "API key created successfully"}

@app.delete("/admin/api-keys/{api_key}")
async def delete_api_key(request: Request, api_key: str, admin_user: str = Depends(verify_admin_session)):
    """Delete API key"""
    if api_key in API_KEYS:
        del API_KEYS[api_key]
        return {"message": "API key deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="API key not found")

@app.get("/admin/domains")
async def get_domains(request: Request, admin_user: str = Depends(verify_admin_session)):
    """Get authorized domains"""
    return {"domains": list(AUTHORIZED_DOMAINS)}

@app.post("/admin/domains")
async def add_domain(request: Request, domain_data: DomainRequest, admin_user: str = Depends(verify_admin_session)):
    """Add authorized domain"""
    AUTHORIZED_DOMAINS.add(domain_data.domain)
    return {"message": f"Domain {domain_data.domain} added successfully"}

@app.delete("/admin/domains/{domain}")
async def delete_domain(request: Request, domain: str, admin_user: str = Depends(verify_admin_session)):
    """Remove authorized domain"""
    if domain in AUTHORIZED_DOMAINS:
        AUTHORIZED_DOMAINS.remove(domain)
        return {"message": f"Domain {domain} removed successfully"}
    else:
        raise HTTPException(status_code=404, detail="Domain not found")

@app.get("/ayanamsha-options")
async def get_ayanamsha_options():
    """Get available ayanamsha options"""
    return {"options": AYANAMSHA_OPTIONS}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "ephe_path": ephe_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)