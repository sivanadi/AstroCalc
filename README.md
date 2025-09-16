# Vedic Astrology Calculator API

A FastAPI web application that calculates Vedic astrology planetary longitudes and Ascendant using Swiss Ephemeris with Lahiri sidereal mode.

## Features

- Calculate Ascendant in Lahiri sidereal mode using Placidus house system
- Compute sidereal longitudes for all 9 Vedic planets: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, and Ketu
- Julian Day conversion for accurate astronomical calculations
- JSON API responses with rounded degree values
- Built-in input validation and error handling

## Usage

### Start the Server

The server runs automatically on port 5000. You can also start it manually:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### API Endpoints

#### GET /chart

Calculate a Vedic astrology chart for a given date, time, and location.

**Parameters:**
- `year` (int): Year (e.g., 2024)
- `month` (int): Month (1-12)
- `day` (int): Day (1-31)
- `hour` (float): Hour in UT decimal format (e.g., 15.5 for 3:30 PM UTC)
- `lat` (float): Latitude in degrees (positive for North)
- `lon` (float): Longitude in degrees (positive for East)

**Example URL:**
```
http://localhost:5000/chart?year=2024&month=1&day=15&hour=12.0&lat=28.6139&lon=77.2090
```

**Using curl:**
```bash
curl "http://localhost:5000/chart?year=2024&month=1&day=15&hour=12.0&lat=28.6139&lon=77.2090"
```

**Example Response:**
```json
{
  "julian_day_ut": 2460325.0,
  "ascendant_deg": 88.14,
  "planets_deg": {
    "Sun": 270.63,
    "Moon": 325.7,
    "Mars": 253.95,
    "Mercury": 247.34,
    "Jupiter": 11.8,
    "Venus": 236.14,
    "Saturn": 310.45,
    "Rahu": 355.92,
    "Ketu": 175.92
  }
}
```

#### GET /health

Health check endpoint to verify API status and ephemeris path.

**Example Response:**
```json
{
  "status": "healthy",
  "ephe_path": "/home/runner/workspace/ephe"
}
```

## Technical Details

- **Sidereal System**: N.C. Lahiri ayanamsha
- **House System**: Placidus
- **Coordinate System**: All positions in degrees (0-360°)
- **Time Format**: Universal Time (UT) in decimal hours
- **Rahu Calculation**: Mean North Node (not True Node)
- **Ketu Calculation**: Rahu + 180° (opposite point)

## Requirements

- Python 3.11+
- FastAPI
- Uvicorn
- pyswisseph
- Swiss Ephemeris data files (included in `ephe/` directory)

## Notes

- All calculations use the Swiss Ephemeris for high astronomical accuracy
- Time input must be in Universal Time (UT), not local time
- Geographic coordinates should be in decimal degrees
- Results are rounded to 2 decimal places for practical use