# Vedic Astrology Calculator API

## Overview

This is a FastAPI web application that provides Vedic astrology calculations using the Swiss Ephemeris library. The application calculates planetary longitudes and Ascendant positions using various sidereal systems (ayanamsas). The API accepts birth data (date, time, and coordinates) and returns precise astronomical calculations for both natal and transit chart generation with flexible ayanamsha support.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

**September 18, 2025 - Successfully imported and configured for Replit environment:**
- Installed all Python dependencies using uv package manager
- Configured FastAPI server workflow to run on port 5000 with proper host configuration
- Disabled API key enforcement for development and added Replit domain to authorized domains
- Tested API endpoints and verified database initialization works correctly
- Configured deployment settings for production using autoscale deployment target
- Application is now fully functional in Replit environment with frontend and API working

## System Architecture

### Core Framework
- **FastAPI**: Chosen for its modern async capabilities, automatic API documentation, and built-in validation
- **Python**: Selected for its rich astronomical libraries and ease of integration with Swiss Ephemeris

### Astronomical Engine
- **Swiss Ephemeris (swisseph)**: Industry-standard astronomical calculation library providing high-precision planetary positions
- **Lahiri Sidereal Mode**: Configured specifically for Vedic astrology calculations using the most widely accepted ayanamsa
- **Placidus House System**: Used for Ascendant calculations, a traditional system in Western and Vedic astrology

### API Design
- **RESTful Architecture**: Single endpoint `/chart` that accepts query parameters for birth data
- **JSON Responses**: Structured data format suitable for frontend integration or third-party consumption
- **Input Validation**: Built-in FastAPI validation for required parameters and data types
- **Error Handling**: HTTPException responses for invalid inputs or calculation errors

### Data Processing
- **Julian Day Conversion**: Converts Gregorian calendar dates to Julian Day numbers for astronomical accuracy
- **Coordinate System**: Accepts standard latitude/longitude coordinates with proper sign conventions
- **UTC Time Handling**: Uses Universal Time for consistent calculations regardless of local time zones
- **Precision Control**: Rounds calculated degrees to reasonable precision for practical use

### Planetary Calculations
- **Nine Vedic Planets**: Supports Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu (North Node), and Ketu (South Node)
- **Sidereal Longitude**: All positions calculated in sidereal zodiac system rather than tropical
- **Mean Node Calculation**: Uses mean positions for lunar nodes (Rahu/Ketu) for consistency with traditional Vedic methods

## External Dependencies

### Astronomical Libraries
- **swisseph**: Swiss Ephemeris Python binding for planetary calculations
- **pytz**: Timezone handling and UTC conversions (though primarily using UTC input)

### Web Framework
- **FastAPI**: Modern Python web framework with automatic API documentation
- **uvicorn**: ASGI server for running the FastAPI application

### Ephemeris Data
- **Swiss Ephemeris Data Files**: Required ephemeris files stored in `/ephe` directory for astronomical calculations
- **File System Access**: Application reads ephemeris data files during initialization and calculations

### Development Tools
- **Python Standard Library**: datetime, os, and typing modules for core functionality
- **JSON Responses**: Built-in FastAPI JSON response handling for API output