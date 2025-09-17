# Vedic Astrology Calculator API - Complete Usage Guide

This comprehensive guide provides step-by-step instructions for making API calls to the Vedic Astrology Calculator using both GET and POST methods across different platforms.

## Table of Contents
- [Getting Started](#getting-started)
- [Authentication Methods](#authentication-methods)
- [GET Method Usage](#get-method-usage)
- [POST Method Usage](#post-method-usage)
- [Platform-Specific Examples](#platform-specific-examples)
- [Next.js Integration](#nextjs-integration)
- [Advanced Use Cases](#advanced-use-cases)
- [Error Handling](#error-handling)
- [Response Parsing](#response-parsing)

## Getting Started

### Prerequisites
1. **API Access**: Either an API key or access from an authorized domain
2. **Base URL**: Your API server URL (e.g., `http://localhost:5000` or `https://yourapi.com`)
3. **Birth Data**: Year, month, day, hour, minute, second, latitude, longitude, timezone

### Required Parameters
- `year` (integer): Birth year (e.g., 1990)
- `month` (integer): Birth month (1-12)
- `day` (integer): Birth day (1-31)
- `hour` (integer): Birth hour (0-23)
- `minute` (integer): Birth minute (0-59) [optional, default: 0]
- `second` (integer): Birth second (0-59) [optional, default: 0]
- `lat` (float): Latitude in decimal degrees (positive = North, negative = South)
- `lon` (float): Longitude in decimal degrees (positive = East, negative = West)
- `tz` (string): Timezone identifier (e.g., "Asia/Kolkata", "America/New_York")

### Optional Parameters
- `ayanamsha` (string): Ayanamsha system [default: "lahiri"]
- `house_system` (string): House system [default: "placidus"]
- `natal_ayanamsha` (string): Natal chart ayanamsha (overrides ayanamsha for natal)
- `natal_house_system` (string): Natal chart house system (overrides house_system for natal)
- `transit_ayanamsha` (string): Transit chart ayanamsha (overrides ayanamsha for transit)
- `transit_house_system` (string): Transit chart house system (overrides house_system for transit)

## Authentication Methods

### Method 1: API Key Authentication
Include your API key in the Authorization header:
```
Authorization: Bearer YOUR_API_KEY_HERE
```

### Method 2: Domain Authorization
Access from a pre-authorized domain (no additional headers required).

## GET Method Usage

### Basic GET Request Structure
```
GET /chart?year=YYYY&month=MM&day=DD&hour=HH&minute=MM&second=SS&lat=LAT&lon=LON&tz=TIMEZONE
```

### Step-by-Step GET Implementation

#### Step 1: Construct the URL
```javascript
const baseUrl = 'http://localhost:5000';
const params = new URLSearchParams({
    year: '1990',
    month: '5',
    day: '15',
    hour: '14',
    minute: '30',
    second: '0',
    lat: '28.6139',
    lon: '77.2090',
    tz: 'Asia/Kolkata',
    ayanamsha: 'lahiri',
    house_system: 'placidus'
});
const url = `${baseUrl}/chart?${params.toString()}`;
```

#### Step 2: Add Authentication (if using API key)
```javascript
const headers = {
    'Authorization': 'Bearer YOUR_API_KEY_HERE'
};
```

#### Step 3: Make the Request
```javascript
fetch(url, { headers })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
```

### GET Examples by Platform

#### **cURL (Command Line)**

**Basic Chart:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY_HERE" \
     "http://localhost:5000/chart?year=1990&month=5&day=15&hour=14&minute=30&second=0&lat=28.6139&lon=77.2090&tz=Asia/Kolkata"
```

**Advanced Chart with Custom Settings:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY_HERE" \
     "http://localhost:5000/chart?year=1990&month=5&day=15&hour=14&minute=30&lat=28.6139&lon=77.2090&tz=Asia/Kolkata&ayanamsha=krishnamurti&house_system=equal&natal_ayanamsha=lahiri&transit_ayanamsha=raman"
```

**Without API Key (from authorized domain):**
```bash
curl "http://localhost:5000/chart?year=1990&month=5&day=15&hour=14&minute=30&lat=28.6139&lon=77.2090&tz=Asia/Kolkata"
```

#### **JavaScript (Browser/Node.js)**

**Basic Implementation:**
```javascript
async function calculateChart() {
    const params = {
        year: 1990,
        month: 5,
        day: 15,
        hour: 14,
        minute: 30,
        second: 0,
        lat: 28.6139,
        lon: 77.2090,
        tz: 'Asia/Kolkata'
    };
    
    const queryString = new URLSearchParams(params).toString();
    const url = `http://localhost:5000/chart?${queryString}`;
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer YOUR_API_KEY_HERE',
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Chart Data:', data);
        return data;
    } catch (error) {
        console.error('Error calculating chart:', error);
        throw error;
    }
}

// Usage
calculateChart().then(data => {
    console.log('Natal Chart:', data.natal_chart);
    console.log('Transit Chart:', data.transit_chart);
});
```

**jQuery Implementation:**
```javascript
function calculateChartJQuery() {
    $.ajax({
        url: 'http://localhost:5000/chart',
        method: 'GET',
        headers: {
            'Authorization': 'Bearer YOUR_API_KEY_HERE'
        },
        data: {
            year: 1990,
            month: 5,
            day: 15,
            hour: 14,
            minute: 30,
            second: 0,
            lat: 28.6139,
            lon: 77.2090,
            tz: 'Asia/Kolkata',
            ayanamsha: 'lahiri'
        },
        success: function(data) {
            console.log('Success:', data);
            // Process the chart data
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
}
```

#### **Python**

**Using requests library:**
```python
import requests
from urllib.parse import urlencode

def calculate_chart_get():
    # Base URL
    base_url = 'http://localhost:5000/chart'
    
    # Parameters
    params = {
        'year': 1990,
        'month': 5,
        'day': 15,
        'hour': 14,
        'minute': 30,
        'second': 0,
        'lat': 28.6139,
        'lon': 77.2090,
        'tz': 'Asia/Kolkata',
        'ayanamsha': 'lahiri',
        'house_system': 'placidus'
    }
    
    # Headers with API key
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY_HERE'
    }
    
    try:
        # Make GET request
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse JSON response
        data = response.json()
        
        print("Chart calculation successful!")
        print(f"Natal Chart Ascendant: {data['natal_chart']['ascendant_deg']}°")
        print(f"Transit Chart Ascendant: {data['transit_chart']['ascendant_deg']}°")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected response format: {e}")
        return None

# Usage
chart_data = calculate_chart_get()
if chart_data:
    print("Planets in Natal Chart:")
    for planet, position in chart_data['natal_chart']['planets_deg'].items():
        print(f"  {planet}: {position}°")
```

#### **PHP**

```php
<?php
function calculateChart() {
    $baseUrl = 'http://localhost:5000/chart';
    
    $params = [
        'year' => 1990,
        'month' => 5,
        'day' => 15,
        'hour' => 14,
        'minute' => 30,
        'second' => 0,
        'lat' => 28.6139,
        'lon' => 77.2090,
        'tz' => 'Asia/Kolkata',
        'ayanamsha' => 'lahiri'
    ];
    
    $url = $baseUrl . '?' . http_build_query($params);
    
    $headers = [
        'Authorization: Bearer YOUR_API_KEY_HERE',
        'Content-Type: application/json'
    ];
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    if ($error) {
        throw new Exception("cURL Error: " . $error);
    }
    
    if ($httpCode !== 200) {
        throw new Exception("HTTP Error: " . $httpCode);
    }
    
    $data = json_decode($response, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("JSON Decode Error: " . json_last_error_msg());
    }
    
    return $data;
}

// Usage
try {
    $chartData = calculateChart();
    echo "Chart calculation successful!\n";
    echo "Natal Ascendant: " . $chartData['natal_chart']['ascendant_deg'] . "°\n";
    
    echo "Natal Planets:\n";
    foreach ($chartData['natal_chart']['planets_deg'] as $planet => $position) {
        echo "  $planet: $position°\n";
    }
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
?>
```

## POST Method Usage

### Basic POST Request Structure
The POST method sends data in the request body as JSON, making it more suitable for complex requests and programmatic access.

### Step-by-Step POST Implementation

#### Step 1: Prepare the Data
```javascript
const chartData = {
    year: 1990,
    month: 5,
    day: 15,
    hour: 14,
    minute: 30,
    second: 0,
    lat: 28.6139,
    lon: 77.2090,
    tz: 'Asia/Kolkata',
    ayanamsha: 'lahiri',
    house_system: 'placidus'
};
```

#### Step 2: Set Headers
```javascript
const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY_HERE'
};
```

#### Step 3: Make the Request
```javascript
fetch('http://localhost:5000/chart', {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(chartData)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### POST Examples by Platform

#### **cURL (Command Line)**

**Basic Chart:**
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_API_KEY_HERE" \
     -d '{
       "year": 1990,
       "month": 5,
       "day": 15,
       "hour": 14,
       "minute": 30,
       "second": 0,
       "lat": 28.6139,
       "lon": 77.2090,
       "tz": "Asia/Kolkata",
       "ayanamsha": "lahiri"
     }' \
     http://localhost:5000/chart
```

**Advanced Chart with Separate Natal/Transit Settings:**
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_API_KEY_HERE" \
     -d '{
       "year": 1990,
       "month": 5,
       "day": 15,
       "hour": 14,
       "minute": 30,
       "second": 0,
       "lat": 28.6139,
       "lon": 77.2090,
       "tz": "Asia/Kolkata",
       "natal_ayanamsha": "lahiri",
       "natal_house_system": "placidus",
       "transit_ayanamsha": "krishnamurti",
       "transit_house_system": "equal"
     }' \
     http://localhost:5000/chart
```

#### **JavaScript (Browser/Node.js)**

**Modern async/await approach:**
```javascript
async function calculateChartPost(birthData) {
    const url = 'http://localhost:5000/chart';
    
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_API_KEY_HERE'
        },
        body: JSON.stringify(birthData)
    };
    
    try {
        const response = await fetch(url, requestOptions);
        
        // Check if request was successful
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(`HTTP ${response.status}: ${errorData.detail || response.statusText}`);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Usage examples
const birthData1 = {
    year: 1990,
    month: 5,
    day: 15,
    hour: 14,
    minute: 30,
    second: 0,
    lat: 28.6139,
    lon: 77.2090,
    tz: 'Asia/Kolkata'
};

const birthData2 = {
    year: 1985,
    month: 12,
    day: 25,
    hour: 8,
    minute: 45,
    lat: 40.7128,
    lon: -74.0060,
    tz: 'America/New_York',
    natal_ayanamsha: 'lahiri',
    natal_house_system: 'placidus',
    transit_ayanamsha: 'krishnamurti',
    transit_house_system: 'equal'
};

// Calculate charts
calculateChartPost(birthData1)
    .then(data => {
        console.log('Chart 1 calculated successfully');
        console.log('Natal planets:', data.natal_chart.planets_deg);
    })
    .catch(error => console.error('Chart 1 failed:', error));

calculateChartPost(birthData2)
    .then(data => {
        console.log('Chart 2 calculated successfully');
        console.log('Different ayanamshas used:');
        console.log('Natal:', data.natal_chart.ayanamsha_name);
        console.log('Transit:', data.transit_chart.ayanamsha_name);
    })
    .catch(error => console.error('Chart 2 failed:', error));
```

**Promise-based approach:**
```javascript
function calculateChartPromise(birthData) {
    return new Promise((resolve, reject) => {
        fetch('http://localhost:5000/chart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_API_KEY_HERE'
            },
            body: JSON.stringify(birthData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => Promise.reject(err));
            }
            return response.json();
        })
        .then(data => resolve(data))
        .catch(error => reject(error));
    });
}
```

#### **Python**

**Complete implementation with error handling:**
```python
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional

class VedicAstrologyAPI:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        
    def _get_headers(self) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers
    
    def calculate_chart(self, birth_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate Vedic astrology chart using POST method
        
        Args:
            birth_data: Dictionary containing birth information
            
        Returns:
            Dictionary containing natal and transit chart data
        """
        url = f'{self.base_url}/chart'
        headers = self._get_headers()
        
        try:
            response = requests.post(url, json=birth_data, headers=headers, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            raise Exception("Connection error. Please check the server URL.")
        except requests.exceptions.HTTPError as e:
            try:
                error_data = response.json()
                raise Exception(f"API Error {response.status_code}: {error_data.get('detail', str(e))}")
            except json.JSONDecodeError:
                raise Exception(f"HTTP Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def get_ayanamsha_options(self) -> Dict[str, str]:
        """Get available ayanamsha options"""
        url = f'{self.base_url}/ayanamsha-options'
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to get ayanamsha options: {str(e)}")

# Usage examples
def main():
    # Initialize API client
    api = VedicAstrologyAPI('http://localhost:5000', 'YOUR_API_KEY_HERE')
    
    # Example 1: Basic chart calculation
    birth_data_1 = {
        'year': 1990,
        'month': 5,
        'day': 15,
        'hour': 14,
        'minute': 30,
        'second': 0,
        'lat': 28.6139,
        'lon': 77.2090,
        'tz': 'Asia/Kolkata',
        'ayanamsha': 'lahiri'
    }
    
    # Example 2: Advanced chart with different systems
    birth_data_2 = {
        'year': 1985,
        'month': 12,
        'day': 25,
        'hour': 8,
        'minute': 45,
        'lat': 51.5074,
        'lon': -0.1278,
        'tz': 'Europe/London',
        'natal_ayanamsha': 'lahiri',
        'natal_house_system': 'placidus',
        'transit_ayanamsha': 'krishnamurti',
        'transit_house_system': 'equal'
    }
    
    try:
        # Get available options first
        print("Getting available ayanamsha options...")
        options = api.get_ayanamsha_options()
        print(f"Available ayanamshas: {list(options.keys())[:5]}...")  # Show first 5
        
        # Calculate first chart
        print("\nCalculating Chart 1...")
        chart1 = api.calculate_chart(birth_data_1)
        
        print("Chart 1 Results:")
        print(f"  Natal Ascendant: {chart1['natal_chart']['ascendant_deg']}°")
        print(f"  Ayanamsha: {chart1['natal_chart']['ayanamsha_name']}")
        print(f"  House System: {chart1['natal_chart']['house_system_name']}")
        
        print("  Natal Planets:")
        for planet, position in chart1['natal_chart']['planets_deg'].items():
            print(f"    {planet}: {position}°")
        
        # Calculate second chart
        print("\nCalculating Chart 2...")
        chart2 = api.calculate_chart(birth_data_2)
        
        print("Chart 2 Results:")
        print("  Natal Chart:")
        print(f"    Ascendant: {chart2['natal_chart']['ascendant_deg']}°")
        print(f"    Ayanamsha: {chart2['natal_chart']['ayanamsha_name']}")
        print(f"    House System: {chart2['natal_chart']['house_system_name']}")
        
        print("  Transit Chart:")
        print(f"    Ascendant: {chart2['transit_chart']['ascendant_deg']}°")
        print(f"    Ayanamsha: {chart2['transit_chart']['ayanamsha_name']}")
        print(f"    House System: {chart2['transit_chart']['house_system_name']}")
        
        # Show difference in planetary positions due to different ayanamshas
        print("\n  Planetary Position Differences (Natal vs Transit ayanamsha):")
        for planet in chart2['natal_chart']['planets_deg']:
            natal_pos = chart2['natal_chart']['planets_deg'][planet]
            transit_pos = chart2['transit_chart']['planets_deg'][planet]
            diff = round(natal_pos - transit_pos, 2)
            print(f"    {planet}: {diff}° difference")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

#### **PHP**

**Complete PHP implementation:**
```php
<?php

class VedicAstrologyAPI {
    private $baseUrl;
    private $apiKey;
    
    public function __construct($baseUrl, $apiKey = null) {
        $this->baseUrl = rtrim($baseUrl, '/');
        $this->apiKey = $apiKey;
    }
    
    private function getHeaders() {
        $headers = [
            'Content-Type: application/json'
        ];
        
        if ($this->apiKey) {
            $headers[] = 'Authorization: Bearer ' . $this->apiKey;
        }
        
        return $headers;
    }
    
    public function calculateChart($birthData) {
        $url = $this->baseUrl . '/chart';
        $headers = $this->getHeaders();
        $jsonData = json_encode($birthData);
        
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $url,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $jsonData,
            CURLOPT_HTTPHEADER => $headers,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_CONNECTTIMEOUT => 10
        ]);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        
        if ($error) {
            throw new Exception("cURL Error: " . $error);
        }
        
        if ($httpCode >= 400) {
            $errorData = json_decode($response, true);
            $message = isset($errorData['detail']) ? $errorData['detail'] : "HTTP Error $httpCode";
            throw new Exception($message);
        }
        
        $data = json_decode($response, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            throw new Exception("JSON Decode Error: " . json_last_error_msg());
        }
        
        return $data;
    }
    
    public function getAyanamshaOptions() {
        $url = $this->baseUrl . '/ayanamsha-options';
        $headers = $this->getHeaders();
        
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $url,
            CURLOPT_HTTPHEADER => $headers,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 10
        ]);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode !== 200) {
            throw new Exception("Failed to get ayanamsha options");
        }
        
        return json_decode($response, true);
    }
}

// Usage examples
try {
    $api = new VedicAstrologyAPI('http://localhost:5000', 'YOUR_API_KEY_HERE');
    
    // Basic chart data
    $birthData1 = [
        'year' => 1990,
        'month' => 5,
        'day' => 15,
        'hour' => 14,
        'minute' => 30,
        'second' => 0,
        'lat' => 28.6139,
        'lon' => 77.2090,
        'tz' => 'Asia/Kolkata',
        'ayanamsha' => 'lahiri'
    ];
    
    // Advanced chart data
    $birthData2 = [
        'year' => 1985,
        'month' => 12,
        'day' => 25,
        'hour' => 8,
        'minute' => 45,
        'lat' => 40.7128,
        'lon' => -74.0060,
        'tz' => 'America/New_York',
        'natal_ayanamsha' => 'lahiri',
        'natal_house_system' => 'placidus',
        'transit_ayanamsha' => 'krishnamurti',
        'transit_house_system' => 'equal'
    ];
    
    // Get available options
    echo "Getting ayanamsha options...\n";
    $options = $api->getAyanamshaOptions();
    echo "Available ayanamshas: " . implode(', ', array_keys(array_slice($options, 0, 5))) . "...\n\n";
    
    // Calculate first chart
    echo "Calculating Chart 1...\n";
    $chart1 = $api->calculateChart($birthData1);
    
    echo "Chart 1 Results:\n";
    echo "  Natal Ascendant: " . $chart1['natal_chart']['ascendant_deg'] . "°\n";
    echo "  Ayanamsha: " . $chart1['natal_chart']['ayanamsha_name'] . "\n";
    echo "  House System: " . $chart1['natal_chart']['house_system_name'] . "\n";
    
    echo "  Natal Planets:\n";
    foreach ($chart1['natal_chart']['planets_deg'] as $planet => $position) {
        echo "    $planet: $position°\n";
    }
    
    // Calculate second chart
    echo "\nCalculating Chart 2...\n";
    $chart2 = $api->calculateChart($birthData2);
    
    echo "Chart 2 Results:\n";
    echo "  Natal Chart:\n";
    echo "    Ascendant: " . $chart2['natal_chart']['ascendant_deg'] . "°\n";
    echo "    Ayanamsha: " . $chart2['natal_chart']['ayanamsha_name'] . "\n";
    echo "  Transit Chart:\n";
    echo "    Ascendant: " . $chart2['transit_chart']['ascendant_deg'] . "°\n";
    echo "    Ayanamsha: " . $chart2['transit_chart']['ayanamsha_name'] . "\n";
    
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}

?>
```

## Next.js Integration

Next.js provides multiple patterns for API integration. This section covers both the modern App Router and the traditional Pages Router, with examples for Server Components, Client Components, Server Actions, and Route Handlers.

### Prerequisites

First, set up your Next.js project with the necessary dependencies:

```bash
# Create a new Next.js project with TypeScript
npx create-next-app@latest my-astrology-app --typescript --tailwind --eslint --app

# Install additional dependencies
cd my-astrology-app
npm install @types/node

# Create environment variables file
touch .env.local
```

### Environment Variables Setup

```bash
# .env.local
VEDIC_ASTROLOGY_API_URL=http://localhost:5000
VEDIC_ASTROLOGY_API_KEY=your_api_key_here

# For production
# VEDIC_ASTROLOGY_API_URL=https://your-api-domain.com
```

### TypeScript Interfaces

Create shared type definitions for your astrology data:

```typescript
// types/astrology.ts
export interface BirthData {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  second?: number;
  lat: number;
  lon: number;
  tz: string;
  ayanamsha?: string;
  house_system?: string;
  natal_ayanamsha?: string;
  natal_house_system?: string;
  transit_ayanamsha?: string;
  transit_house_system?: string;
}

export interface PlanetPositions {
  Sun: number;
  Moon: number;
  Mars: number;
  Mercury: number;
  Jupiter: number;
  Venus: number;
  Saturn: number;
  Rahu: number;
  Ketu: number;
}

export interface ChartData {
  julian_day_ut: number;
  ascendant_deg: number;
  ascendant_full_precision: number;
  planets_deg: PlanetPositions;
  planets_full_precision: PlanetPositions;
  ayanamsha_name: string;
  ayanamsha_value_decimal: number;
  ayanamsha_value_dms: string;
  house_system_name: string;
}

export interface ApiResponse {
  natal_chart: ChartData;
  transit_chart: ChartData;
  timezone_used: string;
  input_time_ut: number;
}

export interface ApiError {
  detail: string;
  status?: number;
}
```

### Utility Functions

Create API utility functions for reuse across your application:

```typescript
// lib/astrology-api.ts
import { BirthData, ApiResponse, ApiError } from '@/types/astrology';

const API_BASE_URL = process.env.VEDIC_ASTROLOGY_API_URL || 'http://localhost:5000';
const API_KEY = process.env.VEDIC_ASTROLOGY_API_KEY;

class AstrologyApiError extends Error {
  status: number;
  
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'AstrologyApiError';
  }
}

export async function calculateChart(birthData: BirthData): Promise<ApiResponse> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  if (API_KEY) {
    headers['Authorization'] = `Bearer ${API_KEY}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/chart`, {
      method: 'POST',
      headers,
      body: JSON.stringify(birthData),
    });

    if (!response.ok) {
      let errorMessage = `HTTP error! status: ${response.status}`;
      
      try {
        const errorData: ApiError = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch {
        // If JSON parsing fails, use the default message
      }
      
      throw new AstrologyApiError(errorMessage, response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof AstrologyApiError) {
      throw error;
    }
    throw new AstrologyApiError(`Network error: ${error}`, 0);
  }
}

export async function getAyanamshaOptions(): Promise<Record<string, string>> {
  const headers: HeadersInit = {};
  
  if (API_KEY) {
    headers['Authorization'] = `Bearer ${API_KEY}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/ayanamsha-options`, {
      headers,
    });

    if (!response.ok) {
      throw new AstrologyApiError(`Failed to fetch ayanamsha options: ${response.status}`, response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof AstrologyApiError) {
      throw error;
    }
    throw new AstrologyApiError(`Network error: ${error}`, 0);
  }
}
```

## App Router Implementation (Recommended)

The App Router is the modern approach for Next.js applications, offering better performance and developer experience.

### 1. Server Component with Direct API Calls

```typescript
// app/chart/[...params]/page.tsx
import { calculateChart } from '@/lib/astrology-api';
import { BirthData } from '@/types/astrology';
import ChartDisplay from '@/components/ChartDisplay';
import { notFound } from 'next/navigation';

interface PageProps {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

export default async function ChartPage({ searchParams }: PageProps) {
  const params = await searchParams;
  
  // Parse URL parameters
  const year = parseInt(params.year as string);
  const month = parseInt(params.month as string);
  const day = parseInt(params.day as string);
  const hour = parseInt(params.hour as string);
  const minute = parseInt(params.minute as string) || 0;
  const lat = parseFloat(params.lat as string);
  const lon = parseFloat(params.lon as string);
  const tz = params.tz as string;

  // Validate required parameters
  if (!year || !month || !day || !hour || !lat || !lon || !tz) {
    notFound();
  }

  const birthData: BirthData = {
    year,
    month,
    day,
    hour,
    minute,
    lat,
    lon,
    tz,
    ayanamsha: params.ayanamsha as string || 'lahiri',
    house_system: params.house_system as string || 'placidus',
  };

  try {
    // Direct API call in Server Component
    const chartData = await calculateChart(birthData);
    
    return (
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6">Vedic Chart Calculation</h1>
        <ChartDisplay data={chartData} birthData={birthData} />
      </div>
    );
  } catch (error) {
    return (
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6 text-red-600">Error</h1>
        <p className="text-red-500">
          {error instanceof Error ? error.message : 'Failed to calculate chart'}
        </p>
      </div>
    );
  }
}
```

### 2. Server Actions for Form Handling

```typescript
// app/actions/chart-actions.ts
'use server';

import { calculateChart, getAyanamshaOptions } from '@/lib/astrology-api';
import { BirthData } from '@/types/astrology';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function calculateChartAction(formData: FormData) {
  const birthData: BirthData = {
    year: parseInt(formData.get('year') as string),
    month: parseInt(formData.get('month') as string),
    day: parseInt(formData.get('day') as string),
    hour: parseInt(formData.get('hour') as string),
    minute: parseInt(formData.get('minute') as string) || 0,
    second: parseInt(formData.get('second') as string) || 0,
    lat: parseFloat(formData.get('lat') as string),
    lon: parseFloat(formData.get('lon') as string),
    tz: formData.get('tz') as string,
    ayanamsha: formData.get('ayanamsha') as string || 'lahiri',
    house_system: formData.get('house_system') as string || 'placidus',
  };

  try {
    const chartData = await calculateChart(birthData);
    
    // Store result in a way that can be accessed by the results page
    // For simplicity, we'll redirect with URL params
    const params = new URLSearchParams({
      year: birthData.year.toString(),
      month: birthData.month.toString(),
      day: birthData.day.toString(),
      hour: birthData.hour.toString(),
      minute: birthData.minute.toString(),
      lat: birthData.lat.toString(),
      lon: birthData.lon.toString(),
      tz: birthData.tz,
      ayanamsha: birthData.ayanamsha || 'lahiri',
      house_system: birthData.house_system || 'placidus',
    });

    redirect(`/chart?${params.toString()}`);
  } catch (error) {
    // Handle errors appropriately
    throw new Error(error instanceof Error ? error.message : 'Failed to calculate chart');
  }
}

export async function getAyanamshaOptionsAction() {
  try {
    return await getAyanamshaOptions();
  } catch (error) {
    throw new Error('Failed to fetch ayanamsha options');
  }
}
```

### 3. Interactive Form Component

```typescript
// components/ChartForm.tsx
'use client';

import { useState, useTransition } from 'react';
import { calculateChartAction } from '@/app/actions/chart-actions';

export default function ChartForm() {
  const [isPending, startTransition] = useTransition();
  const [errors, setErrors] = useState<string[]>([]);

  const handleSubmit = async (formData: FormData) => {
    setErrors([]);
    
    startTransition(async () => {
      try {
        await calculateChartAction(formData);
      } catch (error) {
        setErrors([error instanceof Error ? error.message : 'An error occurred']);
      }
    });
  };

  return (
    <form action={handleSubmit} className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Calculate Vedic Chart</h2>
      
      {errors.length > 0 && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
          {errors.map((error, index) => (
            <p key={index} className="text-red-600">{error}</p>
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Year</label>
          <input
            type="number"
            name="year"
            min="1800"
            max="2100"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            placeholder="1990"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Month</label>
          <input
            type="number"
            name="month"
            min="1"
            max="12"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            placeholder="5"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Day</label>
          <input
            type="number"
            name="day"
            min="1"
            max="31"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            placeholder="15"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Hour</label>
          <input
            type="number"
            name="hour"
            min="0"
            max="23"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            placeholder="14"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Minute</label>
          <input
            type="number"
            name="minute"
            min="0"
            max="59"
            defaultValue="0"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            placeholder="30"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Second</label>
          <input
            type="number"
            name="second"
            min="0"
            max="59"
            defaultValue="0"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            placeholder="0"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Latitude</label>
          <input
            type="number"
            name="lat"
            step="0.0001"
            min="-90"
            max="90"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            placeholder="28.6139"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Longitude</label>
          <input
            type="number"
            name="lon"
            step="0.0001"
            min="-180"
            max="180"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            placeholder="77.2090"
          />
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Timezone</label>
        <input
          type="text"
          name="tz"
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          placeholder="Asia/Kolkata"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">Ayanamsha</label>
          <select name="ayanamsha" defaultValue="lahiri" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
            <option value="lahiri">Lahiri</option>
            <option value="krishnamurti">Krishnamurti</option>
            <option value="raman">Raman</option>
            <option value="yukteshwar">Yukteshwar</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">House System</label>
          <select name="house_system" defaultValue="placidus" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
            <option value="placidus">Placidus</option>
            <option value="equal">Equal House</option>
            <option value="topocentric">Topocentric</option>
            <option value="sripati">Sripati</option>
          </select>
        </div>
      </div>

      <button
        type="submit"
        disabled={isPending}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {isPending ? 'Calculating...' : 'Calculate Chart'}
      </button>
    </form>
  );
}
```

### 4. Route Handler for External API Calls

```typescript
// app/api/chart/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { calculateChart } from '@/lib/astrology-api';
import { BirthData } from '@/types/astrology';

export async function POST(request: NextRequest) {
  try {
    const birthData: BirthData = await request.json();
    
    // Validate required fields
    const requiredFields = ['year', 'month', 'day', 'hour', 'lat', 'lon', 'tz'];
    for (const field of requiredFields) {
      if (!(field in birthData)) {
        return NextResponse.json(
          { error: `Missing required field: ${field}` },
          { status: 400 }
        );
      }
    }

    const chartData = await calculateChart(birthData);
    
    return NextResponse.json(chartData);
  } catch (error) {
    console.error('Chart calculation error:', error);
    
    if (error instanceof Error && error.message.includes('Rate limit')) {
      return NextResponse.json(
        { error: 'Rate limit exceeded. Please try again later.' },
        { status: 429 }
      );
    }

    return NextResponse.json(
      { error: 'Failed to calculate chart' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    
    const birthData: BirthData = {
      year: parseInt(searchParams.get('year') || '0'),
      month: parseInt(searchParams.get('month') || '0'),
      day: parseInt(searchParams.get('day') || '0'),
      hour: parseInt(searchParams.get('hour') || '0'),
      minute: parseInt(searchParams.get('minute') || '0'),
      second: parseInt(searchParams.get('second') || '0'),
      lat: parseFloat(searchParams.get('lat') || '0'),
      lon: parseFloat(searchParams.get('lon') || '0'),
      tz: searchParams.get('tz') || '',
      ayanamsha: searchParams.get('ayanamsha') || 'lahiri',
      house_system: searchParams.get('house_system') || 'placidus',
    };

    const chartData = await calculateChart(birthData);
    
    return NextResponse.json(chartData);
  } catch (error) {
    console.error('Chart calculation error:', error);
    
    return NextResponse.json(
      { error: 'Failed to calculate chart' },
      { status: 500 }
    );
  }
}
```

### 5. Custom Hook for Client-Side API Calls

```typescript
// hooks/useAstrologyApi.ts
'use client';

import { useState, useCallback } from 'react';
import { BirthData, ApiResponse } from '@/types/astrology';

interface UseAstrologyApiReturn {
  data: ApiResponse | null;
  loading: boolean;
  error: string | null;
  calculateChart: (birthData: BirthData) => Promise<void>;
  reset: () => void;
}

export function useAstrologyApi(): UseAstrologyApiReturn {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const calculateChart = useCallback(async (birthData: BirthData) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/chart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(birthData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const chartData = await response.json();
      setData(chartData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return {
    data,
    loading,
    error,
    calculateChart,
    reset,
  };
}
```

### 6. Interactive Client Component with Hook

```typescript
// components/InteractiveChartCalculator.tsx
'use client';

import { useState } from 'react';
import { useAstrologyApi } from '@/hooks/useAstrologyApi';
import { BirthData } from '@/types/astrology';
import ChartDisplay from './ChartDisplay';

export default function InteractiveChartCalculator() {
  const { data, loading, error, calculateChart, reset } = useAstrologyApi();
  const [formData, setFormData] = useState<Partial<BirthData>>({
    ayanamsha: 'lahiri',
    house_system: 'placidus',
    minute: 0,
    second: 0,
  });

  const handleInputChange = (field: keyof BirthData, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: typeof value === 'string' ? value : Number(value),
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const birthData: BirthData = {
      year: formData.year!,
      month: formData.month!,
      day: formData.day!,
      hour: formData.hour!,
      minute: formData.minute || 0,
      second: formData.second || 0,
      lat: formData.lat!,
      lon: formData.lon!,
      tz: formData.tz!,
      ayanamsha: formData.ayanamsha || 'lahiri',
      house_system: formData.house_system || 'placidus',
    };

    await calculateChart(birthData);
  };

  const handleReset = () => {
    reset();
    setFormData({
      ayanamsha: 'lahiri',
      house_system: 'placidus',
      minute: 0,
      second: 0,
    });
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Vedic Astrology Calculator</h1>
      
      {!data ? (
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md">
          {/* Form fields similar to ChartForm component */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <input
              type="number"
              placeholder="Year"
              value={formData.year || ''}
              onChange={(e) => handleInputChange('year', e.target.value)}
              required
              className="rounded-md border-gray-300 shadow-sm"
            />
            <input
              type="number"
              placeholder="Month"
              value={formData.month || ''}
              onChange={(e) => handleInputChange('month', e.target.value)}
              required
              className="rounded-md border-gray-300 shadow-sm"
            />
            <input
              type="number"
              placeholder="Day"
              value={formData.day || ''}
              onChange={(e) => handleInputChange('day', e.target.value)}
              required
              className="rounded-md border-gray-300 shadow-sm"
            />
          </div>
          
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Calculating...' : 'Calculate Chart'}
          </button>
        </form>
      ) : (
        <div>
          <div className="mb-4">
            <button
              onClick={handleReset}
              className="bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700"
            >
              Calculate Another Chart
            </button>
          </div>
          <ChartDisplay data={data} />
        </div>
      )}
    </div>
  );
}
```

## Pages Router Implementation (Legacy)

For projects using the Pages Router, here are the equivalent implementations:

### 1. API Routes

```typescript
// pages/api/chart.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { calculateChart } from '@/lib/astrology-api';
import { BirthData, ApiResponse } from '@/types/astrology';

type Data = ApiResponse | { error: string };

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  if (req.method === 'POST') {
    try {
      const birthData: BirthData = req.body;
      const chartData = await calculateChart(birthData);
      res.status(200).json(chartData);
    } catch (error) {
      console.error('Chart calculation error:', error);
      res.status(500).json({ error: 'Failed to calculate chart' });
    }
  } else if (req.method === 'GET') {
    try {
      const {
        year, month, day, hour, minute = '0', second = '0',
        lat, lon, tz, ayanamsha = 'lahiri', house_system = 'placidus'
      } = req.query;

      const birthData: BirthData = {
        year: parseInt(year as string),
        month: parseInt(month as string),
        day: parseInt(day as string),
        hour: parseInt(hour as string),
        minute: parseInt(minute as string),
        second: parseInt(second as string),
        lat: parseFloat(lat as string),
        lon: parseFloat(lon as string),
        tz: tz as string,
        ayanamsha: ayanamsha as string,
        house_system: house_system as string,
      };

      const chartData = await calculateChart(birthData);
      res.status(200).json(chartData);
    } catch (error) {
      console.error('Chart calculation error:', error);
      res.status(500).json({ error: 'Failed to calculate chart' });
    }
  } else {
    res.setHeader('Allow', ['GET', 'POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
```

### 2. Page Component with SSR

```typescript
// pages/chart.tsx
import { GetServerSideProps, InferGetServerSidePropsType } from 'next';
import { calculateChart } from '@/lib/astrology-api';
import { BirthData, ApiResponse } from '@/types/astrology';
import ChartDisplay from '@/components/ChartDisplay';

interface Props {
  chartData?: ApiResponse;
  error?: string;
  birthData?: BirthData;
}

export default function ChartPage({ 
  chartData, 
  error, 
  birthData 
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  if (error) {
    return (
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6 text-red-600">Error</h1>
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (!chartData) {
    return (
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6">No Chart Data</h1>
        <p>Please provide valid birth data parameters.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Vedic Chart Calculation</h1>
      <ChartDisplay data={chartData} birthData={birthData} />
    </div>
  );
}

export const getServerSideProps: GetServerSideProps<Props> = async (context) => {
  const { query } = context;
  
  try {
    const birthData: BirthData = {
      year: parseInt(query.year as string),
      month: parseInt(query.month as string),
      day: parseInt(query.day as string),
      hour: parseInt(query.hour as string),
      minute: parseInt(query.minute as string) || 0,
      second: parseInt(query.second as string) || 0,
      lat: parseFloat(query.lat as string),
      lon: parseFloat(query.lon as string),
      tz: query.tz as string,
      ayanamsha: query.ayanamsha as string || 'lahiri',
      house_system: query.house_system as string || 'placidus',
    };

    // Validate required parameters
    if (!birthData.year || !birthData.month || !birthData.day || 
        !birthData.hour || !birthData.lat || !birthData.lon || !birthData.tz) {
      return {
        props: {
          error: 'Missing required parameters'
        }
      };
    }

    const chartData = await calculateChart(birthData);
    
    return {
      props: {
        chartData,
        birthData
      }
    };
  } catch (error) {
    return {
      props: {
        error: error instanceof Error ? error.message : 'Failed to calculate chart'
      }
    };
  }
};
```

### Deployment Configuration

Add the following to your `next.config.js`:

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    VEDIC_ASTROLOGY_API_URL: process.env.VEDIC_ASTROLOGY_API_URL,
  },
  // Enable API routes to handle CORS if needed
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          {
            key: 'Access-Control-Allow-Origin',
            value: process.env.NODE_ENV === 'production' 
              ? 'https://yourdomain.com' 
              : '*'
          },
          {
            key: 'Access-Control-Allow-Methods',
            value: 'GET, POST, PUT, DELETE, OPTIONS',
          },
          {
            key: 'Access-Control-Allow-Headers',
            value: 'Content-Type, Authorization',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
```

### Complete Example Usage

Create a complete astrology application:

```typescript
// app/page.tsx
import ChartForm from '@/components/ChartForm';
import { Suspense } from 'react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Vedic Astrology Calculator
          </h1>
          <p className="text-lg text-gray-600">
            Calculate precise planetary positions using Swiss Ephemeris
          </p>
        </div>
        
        <Suspense fallback={<div>Loading form...</div>}>
          <ChartForm />
        </Suspense>
      </div>
    </div>
  );
}
```

This comprehensive Next.js integration covers all modern patterns and provides both Server and Client Component examples, making it easy to integrate the Vedic Astrology Calculator API into any Next.js application.

## Advanced Use Cases

### 1. Comparing Different Ayanamshas

```javascript
async function compareAyanamshas(birthData, ayanamshaList) {
    const results = [];
    
    for (const ayanamsha of ayanamshaList) {
        try {
            const data = { ...birthData, ayanamsha: ayanamsha };
            const result = await fetch('http://localhost:5000/chart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer YOUR_API_KEY_HERE'
                },
                body: JSON.stringify(data)
            });
            
            const chartData = await result.json();
            results.push({
                ayanamsha: ayanamsha,
                ayanamsha_name: chartData.natal_chart.ayanamsha_name,
                sun_position: chartData.natal_chart.planets_deg.Sun,
                ascendant: chartData.natal_chart.ascendant_deg
            });
        } catch (error) {
            console.error(`Error with ${ayanamsha}:`, error);
        }
    }
    
    return results;
}

// Usage
const birthData = {
    year: 1990, month: 5, day: 15, hour: 14, minute: 30,
    lat: 28.6139, lon: 77.2090, tz: 'Asia/Kolkata'
};

const ayanamshas = ['lahiri', 'krishnamurti', 'raman', 'yukteshwar'];
compareAyanamshas(birthData, ayanamshas).then(results => {
    console.log('Ayanamsha Comparison:');
    results.forEach(result => {
        console.log(`${result.ayanamsha_name}: Sun ${result.sun_position}°, ASC ${result.ascendant}°`);
    });
});
```

### 2. Batch Chart Calculations

```python
import asyncio
import aiohttp
import json

async def calculate_multiple_charts(birth_data_list, api_key):
    """Calculate multiple charts asynchronously"""
    
    async def calculate_single_chart(session, birth_data):
        url = 'http://localhost:5000/chart'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        try:
            async with session.post(url, json=birth_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {'success': True, 'data': data, 'birth_data': birth_data}
                else:
                    error_text = await response.text()
                    return {'success': False, 'error': error_text, 'birth_data': birth_data}
        except Exception as e:
            return {'success': False, 'error': str(e), 'birth_data': birth_data}
    
    async with aiohttp.ClientSession() as session:
        tasks = [calculate_single_chart(session, bd) for bd in birth_data_list]
        results = await asyncio.gather(*tasks)
    
    return results

# Usage
async def main():
    birth_data_list = [
        {
            'year': 1990, 'month': 5, 'day': 15, 'hour': 14, 'minute': 30,
            'lat': 28.6139, 'lon': 77.2090, 'tz': 'Asia/Kolkata', 'ayanamsha': 'lahiri'
        },
        {
            'year': 1985, 'month': 12, 'day': 25, 'hour': 8, 'minute': 45,
            'lat': 40.7128, 'lon': -74.0060, 'tz': 'America/New_York', 'ayanamsha': 'krishnamurti'
        },
        {
            'year': 1992, 'month': 3, 'day': 10, 'hour': 18, 'minute': 0,
            'lat': 51.5074, 'lon': -0.1278, 'tz': 'Europe/London', 'ayanamsha': 'raman'
        }
    ]
    
    results = await calculate_multiple_charts(birth_data_list, 'YOUR_API_KEY_HERE')
    
    for i, result in enumerate(results):
        if result['success']:
            print(f"Chart {i+1}: Success")
            print(f"  Ascendant: {result['data']['natal_chart']['ascendant_deg']}°")
        else:
            print(f"Chart {i+1}: Failed - {result['error']}")

# Run the async function
asyncio.run(main())
```

### 3. Chart Data Analysis

```javascript
function analyzeChart(chartData) {
    const { natal_chart } = chartData;
    
    // Extract planetary positions
    const planets = natal_chart.planets_deg;
    const ascendant = natal_chart.ascendant_deg;
    
    // Calculate planetary aspects (simple conjunction check - within 10 degrees)
    const conjunctions = [];
    const planetNames = Object.keys(planets);
    
    for (let i = 0; i < planetNames.length; i++) {
        for (let j = i + 1; j < planetNames.length; j++) {
            const planet1 = planetNames[i];
            const planet2 = planetNames[j];
            const pos1 = planets[planet1];
            const pos2 = planets[planet2];
            
            const diff = Math.abs(pos1 - pos2);
            const orb = Math.min(diff, 360 - diff); // Handle zodiac wrap-around
            
            if (orb <= 10) {
                conjunctions.push({
                    planets: [planet1, planet2],
                    orb: orb.toFixed(2)
                });
            }
        }
    }
    
    // Find planets in different zodiac signs
    const zodiacSigns = [
        'Aries', 'Taurus', 'Gemini', 'Cancer',
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ];
    
    const planetSigns = {};
    for (const [planet, position] of Object.entries(planets)) {
        const signIndex = Math.floor(position / 30);
        planetSigns[planet] = zodiacSigns[signIndex];
    }
    
    return {
        conjunctions,
        planetSigns,
        ascendantSign: zodiacSigns[Math.floor(ascendant / 30)],
        ayanamsha: natal_chart.ayanamsha_name,
        houseSystem: natal_chart.house_system_name
    };
}

// Usage with chart calculation
async function calculateAndAnalyze(birthData) {
    try {
        const response = await fetch('http://localhost:5000/chart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_API_KEY_HERE'
            },
            body: JSON.stringify(birthData)
        });
        
        const chartData = await response.json();
        const analysis = analyzeChart(chartData);
        
        console.log('Chart Analysis:');
        console.log(`Ascendant Sign: ${analysis.ascendantSign}`);
        console.log(`Ayanamsha: ${analysis.ayanamsha}`);
        console.log(`House System: ${analysis.houseSystem}`);
        
        console.log('\nPlanetary Signs:');
        for (const [planet, sign] of Object.entries(analysis.planetSigns)) {
            console.log(`  ${planet}: ${sign}`);
        }
        
        console.log('\nConjunctions (within 10°):');
        analysis.conjunctions.forEach(conj => {
            console.log(`  ${conj.planets[0]} - ${conj.planets[1]}: ${conj.orb}° orb`);
        });
        
        return { chartData, analysis };
        
    } catch (error) {
        console.error('Error:', error);
    }
}
```

## Error Handling

### Common Error Responses

#### 1. Authentication Errors (403)
```json
{
    "detail": "Access denied. Valid API key or authorized domain required."
}
```

#### 2. Rate Limit Errors (429)
```json
{
    "detail": "Rate limit exceeded: Per-minute limit exceeded: 60/60"
}
```

#### 3. Validation Errors (400)
```json
{
    "detail": "Month must be between 1 and 12"
}
```

#### 4. Invalid Parameters (400)
```json
{
    "detail": "Invalid ayanamsha. Must be one of: ['lahiri', 'krishnamurti', ...]"
}
```

### Comprehensive Error Handling Example

```javascript
async function robustChartCalculation(birthData, maxRetries = 3) {
    let attempts = 0;
    
    while (attempts < maxRetries) {
        try {
            const response = await fetch('http://localhost:5000/chart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer YOUR_API_KEY_HERE'
                },
                body: JSON.stringify(birthData)
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                
                switch (response.status) {
                    case 400:
                        throw new Error(`Invalid data: ${errorData.detail || 'Bad Request'}`);
                    
                    case 403:
                        throw new Error(`Authentication failed: ${errorData.detail || 'Forbidden'}`);
                    
                    case 429:
                        console.log('Rate limit hit, waiting before retry...');
                        if (attempts < maxRetries - 1) {
                            await new Promise(resolve => setTimeout(resolve, 60000)); // Wait 1 minute
                            attempts++;
                            continue;
                        }
                        throw new Error(`Rate limit exceeded: ${errorData.detail || 'Too Many Requests'}`);
                    
                    case 500:
                        throw new Error(`Server error: ${errorData.detail || 'Internal Server Error'}`);
                    
                    default:
                        throw new Error(`HTTP ${response.status}: ${errorData.detail || response.statusText}`);
                }
            }
            
            const data = await response.json();
            console.log(`Chart calculated successfully after ${attempts + 1} attempt(s)`);
            return data;
            
        } catch (error) {
            attempts++;
            
            if (error.message.includes('Rate limit') && attempts < maxRetries) {
                console.log(`Attempt ${attempts} failed due to rate limit, retrying...`);
                continue;
            }
            
            if (attempts >= maxRetries) {
                throw new Error(`Failed after ${maxRetries} attempts: ${error.message}`);
            }
            
            // For non-rate-limit errors, don't retry
            if (!error.message.includes('Rate limit') && !error.message.includes('Server error')) {
                throw error;
            }
            
            console.log(`Attempt ${attempts} failed: ${error.message}, retrying...`);
            await new Promise(resolve => setTimeout(resolve, 1000 * attempts)); // Progressive delay
        }
    }
}
```

## Response Parsing

### Understanding the Response Structure

The API returns a comprehensive JSON response with both natal and transit chart data:

```javascript
{
    "natal_chart": {
        "julian_day_ut": 2448052.104166667,
        "ascendant_deg": 147.23,
        "ascendant_full_precision": 147.234567,
        "planets_deg": {
            "Sun": 54.12,
            "Moon": 203.45,
            "Mars": 89.67,
            "Mercury": 41.23,
            "Jupiter": 278.90,
            "Venus": 76.54,
            "Saturn": 305.21,
            "Rahu": 156.78,
            "Ketu": 336.78
        },
        "planets_full_precision": {
            // Same planets with 6 decimal precision
        },
        "ayanamsha_name": "N.C. Lahiri",
        "ayanamsha_value_decimal": 23.456789,
        "ayanamsha_value_dms": "23°27'24.44\"",
        "house_system_name": "Placidus"
    },
    "transit_chart": {
        // Similar structure for current planetary positions
    },
    "timezone_used": "Asia/Kolkata",
    "input_time_ut": 14.5  // Input time converted to UT
}
```

### Response Parsing Examples

#### JavaScript/TypeScript Interface

```typescript
interface PlanetPositions {
    Sun: number;
    Moon: number;
    Mars: number;
    Mercury: number;
    Jupiter: number;
    Venus: number;
    Saturn: number;
    Rahu: number;
    Ketu: number;
}

interface ChartData {
    julian_day_ut: number;
    ascendant_deg: number;
    ascendant_full_precision: number;
    planets_deg: PlanetPositions;
    planets_full_precision: PlanetPositions;
    ayanamsha_name: string;
    ayanamsha_value_decimal: number;
    ayanamsha_value_dms: string;
    house_system_name: string;
}

interface APIResponse {
    natal_chart: ChartData;
    transit_chart: ChartData;
    timezone_used: string;
    input_time_ut: number;
}

function parseChartResponse(response: APIResponse): void {
    console.log('=== NATAL CHART ===');
    console.log(`Ascendant: ${response.natal_chart.ascendant_deg}°`);
    console.log(`Ayanamsha: ${response.natal_chart.ayanamsha_name} (${response.natal_chart.ayanamsha_value_dms})`);
    console.log(`House System: ${response.natal_chart.house_system_name}`);
    
    console.log('\nPlanetary Positions:');
    Object.entries(response.natal_chart.planets_deg).forEach(([planet, position]) => {
        console.log(`  ${planet.padEnd(8)}: ${position.toFixed(2)}°`);
    });
    
    console.log('\n=== TRANSIT CHART ===');
    console.log(`Ascendant: ${response.transit_chart.ascendant_deg}°`);
    console.log(`Ayanamsha: ${response.transit_chart.ayanamsha_name}`);
    
    console.log('\nTransit Positions:');
    Object.entries(response.transit_chart.planets_deg).forEach(([planet, position]) => {
        console.log(`  ${planet.padEnd(8)}: ${position.toFixed(2)}°`);
    });
    
    console.log(`\nTimezone: ${response.timezone_used}`);
    console.log(`UT Time: ${response.input_time_ut}`);
}
```

#### Python Response Parser

```python
from dataclasses import dataclass
from typing import Dict

@dataclass
class ChartData:
    julian_day_ut: float
    ascendant_deg: float
    ascendant_full_precision: float
    planets_deg: Dict[str, float]
    planets_full_precision: Dict[str, float]
    ayanamsha_name: str
    ayanamsha_value_decimal: float
    ayanamsha_value_dms: str
    house_system_name: str

def parse_chart_response(response_data: dict) -> None:
    """Parse and display chart response data"""
    
    natal = response_data['natal_chart']
    transit = response_data['transit_chart']
    
    print("=== NATAL CHART ===")
    print(f"Ascendant: {natal['ascendant_deg']}°")
    print(f"Ayanamsha: {natal['ayanamsha_name']} ({natal['ayanamsha_value_dms']})")
    print(f"House System: {natal['house_system_name']}")
    
    print("\nPlanetary Positions:")
    for planet, position in natal['planets_deg'].items():
        zodiac_sign = get_zodiac_sign(position)
        degree_in_sign = position % 30
        print(f"  {planet:<8}: {position:6.2f}° ({zodiac_sign} {degree_in_sign:5.2f}°)")
    
    print("\n=== TRANSIT CHART ===")
    print(f"Ascendant: {transit['ascendant_deg']}°")
    print(f"Ayanamsha: {transit['ayanamsha_name']}")
    
    print("\nTransit Positions:")
    for planet, position in transit['planets_deg'].items():
        zodiac_sign = get_zodiac_sign(position)
        degree_in_sign = position % 30
        natal_position = natal['planets_deg'][planet]
        difference = abs(position - natal_position)
        if difference > 180:
            difference = 360 - difference
        
        print(f"  {planet:<8}: {position:6.2f}° ({zodiac_sign} {degree_in_sign:5.2f}°) [±{difference:5.2f}° from natal]")
    
    print(f"\nTimezone: {response_data['timezone_used']}")
    print(f"UT Time: {response_data['input_time_ut']}")

def get_zodiac_sign(longitude: float) -> str:
    """Convert longitude to zodiac sign"""
    signs = [
        'Aries', 'Taurus', 'Gemini', 'Cancer',
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    return signs[int(longitude // 30)]

# Usage
def main():
    # Assume chart_data is the response from API
    # parse_chart_response(chart_data)
    pass
```

## Best Practices

### 1. API Key Security
- Store API keys in environment variables, not in source code
- Use different API keys for development and production
- Rotate API keys regularly
- Monitor API key usage through the admin panel

### 2. Rate Limit Management
- Implement exponential backoff for rate limit errors
- Cache frequently requested charts to reduce API calls
- Use batch processing for multiple calculations
- Monitor your usage patterns

### 3. Error Handling
- Always implement proper error handling
- Log errors for debugging
- Provide meaningful error messages to users
- Implement retry logic for transient errors

### 4. Performance Optimization
- Use appropriate timeout values
- Implement connection pooling for high-volume applications
- Consider using async/await for multiple requests
- Cache responses when possible

### 5. Data Validation
- Validate birth data before sending requests
- Check coordinate ranges and date validity
- Verify timezone identifiers
- Handle edge cases (leap years, daylight saving time)

This completes the comprehensive API usage guide. Each platform example includes proper error handling, authentication, and demonstrates both basic and advanced usage patterns.