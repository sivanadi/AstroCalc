# Vedic Astrology Calculator API - Complete Usage Guide

This comprehensive guide provides step-by-step instructions for making API calls to the Vedic Astrology Calculator using both GET and POST methods across different platforms.

## Table of Contents
- [Getting Started](#getting-started)
- [Authentication Methods](#authentication-methods)
- [GET Method Usage](#get-method-usage)
- [POST Method Usage](#post-method-usage)
- [Platform-Specific Examples](#platform-specific-examples)
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