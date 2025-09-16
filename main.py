from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import swisseph as swe
import pytz
import os
from datetime import datetime
from typing import Dict, Union

app = FastAPI(title="Vedic Astrology Calculator", description="Calculate planetary longitudes and Ascendant using Swiss Ephemeris")

# Set the ephemeris path
ephe_path = os.path.join(os.getcwd(), "ephe")
swe.set_ephe_path(ephe_path)

# Set sidereal mode to Lahiri
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

@app.get("/")
async def root():
    return {"message": "Vedic Astrology Calculator API", "endpoints": ["/chart"]}

@app.get("/chart")
async def calculate_chart(
    year: int,
    month: int, 
    day: int,
    hour: float,
    lat: float,
    lon: float
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "ephe_path": ephe_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)