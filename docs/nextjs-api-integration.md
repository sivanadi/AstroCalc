# Vedic Astrology Calculator API - Next.js Integration Guide

## Overview

This comprehensive guide demonstrates how to integrate the Vedic Astrology Calculator API with Next.js applications. The API provides high-precision planetary calculations using the Swiss Ephemeris library with multiple authentication methods and extensive configuration options.

## Table of Contents

1. [API Base Information](#api-base-information)
2. [Authentication Methods](#authentication-methods)
3. [Core Endpoints](#core-endpoints)
4. [Data Models & Types](#data-models--types)
5. [Next.js Integration Patterns](#nextjs-integration-patterns)
6. [Usage Examples](#usage-examples)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## API Base Information

**Base URL**: `https://your-api-domain.com` (replace with your actual domain)

### Health Check
```bash
GET /health
```
Returns API health status and ephemeris path configuration.

## Authentication Methods

The API supports multiple authentication approaches for different Next.js deployment scenarios:

### 1. API Key Authentication (Recommended for Production)
- Secure server-side authentication
- Rate limiting per API key
- Usage analytics and monitoring

### 2. Domain Authorization
- Frontend domain-based access control
- Rate limiting per domain
- Suitable for public client-side usage

### 3. Bypass Mode (Development Only)
- Temporary development access
- Should never be used in production

## Available Ayanamsha Systems

The API supports over 40 different ayanamsha systems. Here are the most commonly used ones:

```typescript
const AYANAMSHA_OPTIONS = {
  'lahiri': 'N.C. Lahiri',
  'raman': 'B.V. Raman', 
  'krishnamurti': 'Krishnamurti',
  'yukteshwar': 'Yukteshwar',
  'jn_bhasin': 'J.N. Bhasin',
  'suryasiddhanta': 'Suryasiddhanta',
  'aryabhata': 'Aryabhata',
  'true_citra': 'True Citra',
  'true_revati': 'True Revati',
  // ... and many more
};
```

Fetch all available options dynamically:
```typescript
const response = await fetch(`${API_BASE_URL}/ayanamsha-options`);
const { options } = await response.json();
```

## House Systems

The API supports multiple house systems:

```typescript
const HOUSE_SYSTEMS = {
  'placidus': 'Placidus',
  'equal': 'Equal House',
  'topocentric': 'Topocentric', 
  'sripati': 'Sripati'
};
```

## Supported Planets

The API calculates positions for these celestial bodies:

```typescript
const PLANETS = {
  'Sun': 'Sun',
  'Moon': 'Moon',
  'Mars': 'Mars', 
  'Mercury': 'Mercury',
  'Jupiter': 'Jupiter',
  'Venus': 'Venus',
  'Saturn': 'Saturn',
  'Rahu': 'Rahu (North Node)',
  'Ketu': 'Ketu (South Node)' // Calculated as opposite of Rahu
};
```

## Core Endpoints

### Chart Calculation

#### GET `/chart` - Query Parameters Method
```typescript
// Next.js Server Component or API Route
const response = await fetch(`${API_BASE_URL}/chart?` + new URLSearchParams({
  year: '1990',
  month: '5',
  day: '15',
  hour: '14',
  minute: '30',
  lat: '28.6139',
  lon: '77.2090',
  tz: 'Asia/Kolkata',
  ayanamsha: 'lahiri',
  house_system: 'placidus'
}), {
  headers: {
    'Authorization': `Bearer ${API_KEY}`, // If using API key auth
    'Origin': 'https://yourdomain.com' // If using domain auth
  }
});
```

#### POST `/chart` - JSON Payload Method
```typescript
// More structured approach with TypeScript
interface ChartRequest {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute?: number;
  second?: number;
  lat: number;
  lon: number;
  tz?: string;
  ayanamsha?: string;
  house_system?: string;
  natal_ayanamsha?: string;
  natal_house_system?: string;
  transit_ayanamsha?: string;
  transit_house_system?: string;
}

const chartData: ChartRequest = {
  year: 1990,
  month: 5,
  day: 15,
  hour: 14,
  minute: 30,
  lat: 28.6139,
  lon: 77.2090,
  tz: 'Asia/Kolkata',
  ayanamsha: 'lahiri',
  house_system: 'placidus'
};

const response = await fetch(`${API_BASE_URL}/chart`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`
  },
  body: JSON.stringify(chartData)
});
```

### Information Endpoints

#### GET `/ayanamsha-options`
Retrieve available ayanamsha systems:
```typescript
const response = await fetch(`${API_BASE_URL}/ayanamsha-options`);
const data = await response.json();
// Returns: { options: { "lahiri": "Lahiri", "raman": "Raman", ... } }
```

#### GET `/security-status`
Get API security configuration:
```typescript
const response = await fetch(`${API_BASE_URL}/security-status`);
const data = await response.json();
// Returns security status, session info, and configuration
```

## Data Models & Types

### TypeScript Interfaces

```typescript
// Core Chart Request
interface ChartRequest {
  year: number;
  month: number; // 1-12
  day: number; // 1-31
  hour: number; // 0-23
  minute?: number; // 0-59, default: 0
  second?: number; // 0-59, default: 0
  lat: number; // Latitude in decimal degrees
  lon: number; // Longitude in decimal degrees
  tz?: string; // Timezone (default: 'UTC')
  ayanamsha?: string; // Default: 'lahiri'
  house_system?: string; // Default: 'placidus'
  natal_ayanamsha?: string; // Separate ayanamsha for natal
  natal_house_system?: string; // Separate house system for natal
  transit_ayanamsha?: string; // Separate ayanamsha for transit
  transit_house_system?: string; // Separate house system for transit
}

// Chart Response
interface ChartResponse {
  natal: {
    planets: {
      [planetName: string]: {
        longitude: number;
        sign: string;
        degree: number;
        minute: number;
        second: number;
      }
    };
    houses: {
      [houseNumber: string]: {
        sign: string;
        degree: number;
        minute: number;
        second: number;
      }
    };
    ascendant: {
      longitude: number;
      sign: string;
      degree: number;
      minute: number;
      second: number;
    };
  };
  transit: {
    // Same structure as natal
  };
  metadata: {
    birth_time: string;
    timezone: string;
    ayanamsha: string;
    house_system: string;
    julian_day: number;
  };
}

// Error Response
interface ApiError {
  detail: string;
  status_code?: number;
}

// Admin Models (for admin panel integration)
interface AdminLogin {
  username: string;
  password: string;
}

interface APIKeyRequest {
  name: string;
  description?: string;
  per_minute_limit?: number;
  per_day_limit?: number;
  per_month_limit?: number;
}

interface DomainRequest {
  domain: string;
}
```

## Next.js Integration Patterns

### 1. Server-Side Rendering (SSR) with API Routes

#### pages/api/chart.ts (Pages Router)
```typescript
import type { NextApiRequest, NextApiResponse } from 'next';

const API_BASE_URL = process.env.ASTROLOGY_API_URL;
const API_KEY = process.env.ASTROLOGY_API_KEY;

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const response = await fetch(`${API_BASE_URL}/chart`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify(req.body)
    });

    if (!response.ok) {
      const error = await response.json();
      return res.status(response.status).json(error);
    }

    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    console.error('API Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}
```

#### app/api/chart/route.ts (App Router)
```typescript
import { NextRequest, NextResponse } from 'next/server';

const API_BASE_URL = process.env.ASTROLOGY_API_URL;
const API_KEY = process.env.ASTROLOGY_API_KEY;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    const response = await fetch(`${API_BASE_URL}/chart`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const error = await response.json();
      return NextResponse.json(error, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### 2. Client-Side Integration

#### React Hook for Chart Calculation
```typescript
import { useState, useCallback } from 'react';

interface UseChartCalculation {
  calculateChart: (data: ChartRequest) => Promise<void>;
  chartData: ChartResponse | null;
  loading: boolean;
  error: string | null;
}

export const useChartCalculation = (): UseChartCalculation => {
  const [chartData, setChartData] = useState<ChartResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const calculateChart = useCallback(async (data: ChartRequest) => {
    setLoading(true);
    setError(null);

    try {
      // Use your Next.js API route as a proxy
      const response = await fetch('/api/chart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to calculate chart');
      }

      const result = await response.json();
      setChartData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, []);

  return { calculateChart, chartData, loading, error };
};
```

#### Chart Component Example
```typescript
'use client'; // For App Router

import { useState } from 'react';
import { useChartCalculation } from '@/hooks/useChartCalculation';

interface ChartFormData {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  lat: number;
  lon: number;
  tz: string;
}

export default function ChartCalculator() {
  const { calculateChart, chartData, loading, error } = useChartCalculation();
  const [formData, setFormData] = useState<ChartFormData>({
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
    day: new Date().getDate(),
    hour: 12,
    minute: 0,
    lat: 28.6139,
    lon: 77.2090,
    tz: 'Asia/Kolkata'
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await calculateChart(formData);
  };

  return (
    <div className="chart-calculator">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <input
            type="number"
            placeholder="Year"
            value={formData.year}
            onChange={(e) => setFormData(prev => ({ 
              ...prev, 
              year: parseInt(e.target.value) 
            }))}
            className="px-3 py-2 border rounded"
          />
          <input
            type="number"
            placeholder="Month (1-12)"
            min="1"
            max="12"
            value={formData.month}
            onChange={(e) => setFormData(prev => ({ 
              ...prev, 
              month: parseInt(e.target.value) 
            }))}
            className="px-3 py-2 border rounded"
          />
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          <input
            type="number"
            placeholder="Day"
            min="1"
            max="31"
            value={formData.day}
            onChange={(e) => setFormData(prev => ({ 
              ...prev, 
              day: parseInt(e.target.value) 
            }))}
            className="px-3 py-2 border rounded"
          />
          <input
            type="number"
            placeholder="Hour (0-23)"
            min="0"
            max="23"
            value={formData.hour}
            onChange={(e) => setFormData(prev => ({ 
              ...prev, 
              hour: parseInt(e.target.value) 
            }))}
            className="px-3 py-2 border rounded"
          />
          <input
            type="number"
            placeholder="Minute (0-59)"
            min="0"
            max="59"
            value={formData.minute}
            onChange={(e) => setFormData(prev => ({ 
              ...prev, 
              minute: parseInt(e.target.value) 
            }))}
            className="px-3 py-2 border rounded"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <input
            type="number"
            step="any"
            placeholder="Latitude"
            value={formData.lat}
            onChange={(e) => setFormData(prev => ({ 
              ...prev, 
              lat: parseFloat(e.target.value) 
            }))}
            className="px-3 py-2 border rounded"
          />
          <input
            type="number"
            step="any"
            placeholder="Longitude"
            value={formData.lon}
            onChange={(e) => setFormData(prev => ({ 
              ...prev, 
              lon: parseFloat(e.target.value) 
            }))}
            className="px-3 py-2 border rounded"
          />
        </div>

        <select
          value={formData.tz}
          onChange={(e) => setFormData(prev => ({ ...prev, tz: e.target.value }))}
          className="w-full px-3 py-2 border rounded"
        >
          <option value="UTC">UTC</option>
          <option value="Asia/Kolkata">Asia/Kolkata</option>
          <option value="America/New_York">America/New_York</option>
          <option value="Europe/London">Europe/London</option>
        </select>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Calculating...' : 'Calculate Chart'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          Error: {error}
        </div>
      )}

      {chartData && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-4">Chart Results</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium mb-2">Natal Planets</h4>
              <div className="space-y-2">
                {Object.entries(chartData.natal.planets).map(([planet, data]) => (
                  <div key={planet} className="flex justify-between">
                    <span className="capitalize">{planet}:</span>
                    <span>{data.sign} {data.degree}°{data.minute}'</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-medium mb-2">Houses</h4>
              <div className="space-y-2">
                {Object.entries(chartData.natal.houses).map(([house, data]) => (
                  <div key={house} className="flex justify-between">
                    <span>House {house}:</span>
                    <span>{data.sign} {data.degree}°{data.minute}'</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

### 3. Server Component Integration (App Router)

```typescript
// app/chart/[id]/page.tsx
import { ChartDisplay } from '@/components/ChartDisplay';

async function getChartData(chartId: string) {
  const API_BASE_URL = process.env.ASTROLOGY_API_URL;
  const API_KEY = process.env.ASTROLOGY_API_KEY;

  // Example: Get saved chart data and calculate
  const chartParams = await getSavedChartParams(chartId);
  
  const response = await fetch(`${API_BASE_URL}/chart`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`
    },
    body: JSON.stringify(chartParams),
    // Optional: Add caching
    next: { revalidate: 3600 } // Cache for 1 hour
  });

  if (!response.ok) {
    throw new Error('Failed to fetch chart data');
  }

  return response.json();
}

export default async function ChartPage({ params }: { params: { id: string } }) {
  const chartData = await getChartData(params.id);

  return (
    <div>
      <h1>Vedic Chart Analysis</h1>
      <ChartDisplay data={chartData} />
    </div>
  );
}
```

## Usage Examples

### 1. Basic Birth Chart Calculator

```typescript
// components/BirthChartCalculator.tsx
import { useState } from 'react';

export function BirthChartCalculator() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculateChart = async (birthData) => {
    setLoading(true);
    try {
      const response = await fetch('/api/chart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          year: birthData.year,
          month: birthData.month,
          day: birthData.day,
          hour: birthData.hour,
          minute: birthData.minute,
          lat: birthData.latitude,
          lon: birthData.longitude,
          tz: birthData.timezone,
          ayanamsha: 'lahiri',
          house_system: 'placidus'
        })
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Chart calculation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Birth form here */}
      {result && <ChartDisplay data={result} />}
    </div>
  );
}
```

### 2. Transit Analysis

```typescript
// Calculate current transits for a birth chart
const getTransitAnalysis = async (natalData) => {
  const now = new Date();
  
  const transitRequest = {
    ...natalData,
    // Override with current date/time for transits
    year: now.getFullYear(),
    month: now.getMonth() + 1,
    day: now.getDate(),
    hour: now.getHours(),
    minute: now.getMinutes(),
    natal_ayanamsha: 'lahiri',
    transit_ayanamsha: 'lahiri'
  };

  const response = await fetch('/api/chart', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(transitRequest)
  });

  return response.json();
};
```

### 3. Compatibility Analysis

```typescript
// Compare two birth charts
const getCompatibilityAnalysis = async (person1Data, person2Data) => {
  const [chart1, chart2] = await Promise.all([
    fetch('/api/chart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(person1Data)
    }).then(r => r.json()),
    
    fetch('/api/chart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(person2Data)
    }).then(r => r.json())
  ]);

  // Analyze compatibility using chart data
  return analyzeCompatibility(chart1, chart2);
};
```

### 4. Ayanamsha Comparison

```typescript
// Calculate chart with different ayanamsha systems
const compareAyanamshas = async (birthData) => {
  const ayanamshas = ['lahiri', 'raman', 'krishnamurti'];
  
  const charts = await Promise.all(
    ayanamshas.map(ayanamsha =>
      fetch('/api/chart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...birthData,
          ayanamsha
        })
      }).then(r => r.json())
    )
  );

  return ayanamshas.reduce((acc, ayanamsha, index) => {
    acc[ayanamsha] = charts[index];
    return acc;
  }, {});
};
```

## Error Handling

### Comprehensive Error Handler

```typescript
class AstrologyAPIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code?: string
  ) {
    super(message);
    this.name = 'AstrologyAPIError';
  }
}

const handleAPIResponse = async (response: Response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    
    switch (response.status) {
      case 400:
        throw new AstrologyAPIError(
          errorData.detail || 'Invalid request parameters',
          400,
          'INVALID_REQUEST'
        );
      case 401:
        throw new AstrologyAPIError(
          'Authentication failed - check your API key',
          401,
          'AUTH_FAILED'
        );
      case 403:
        throw new AstrologyAPIError(
          'Access forbidden - domain not authorized',
          403,
          'ACCESS_FORBIDDEN'
        );
      case 429:
        throw new AstrologyAPIError(
          'Rate limit exceeded - please try again later',
          429,
          'RATE_LIMITED'
        );
      case 500:
        throw new AstrologyAPIError(
          'Server error - please try again',
          500,
          'SERVER_ERROR'
        );
      default:
        throw new AstrologyAPIError(
          errorData.detail || 'Unknown error occurred',
          response.status,
          'UNKNOWN_ERROR'
        );
    }
  }
  
  return response.json();
};

// Usage in API calls
const calculateChart = async (data: ChartRequest) => {
  try {
    const response = await fetch('/api/chart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    return await handleAPIResponse(response);
  } catch (error) {
    if (error instanceof AstrologyAPIError) {
      // Handle specific API errors
      console.error(`API Error [${error.code}]:`, error.message);
      throw error;
    } else {
      // Handle network or other errors
      console.error('Network Error:', error);
      throw new AstrologyAPIError('Network error', 0, 'NETWORK_ERROR');
    }
  }
};
```

## Rate Limiting

### Rate Limit Awareness

```typescript
interface RateLimitInfo {
  remaining: number;
  reset: number;
  limit: number;
}

const makeAPICall = async (url: string, options: RequestInit) => {
  const response = await fetch(url, options);
  
  // Check rate limit headers (if implemented)
  const rateLimitInfo: RateLimitInfo = {
    remaining: parseInt(response.headers.get('X-RateLimit-Remaining') || '0'),
    reset: parseInt(response.headers.get('X-RateLimit-Reset') || '0'),
    limit: parseInt(response.headers.get('X-RateLimit-Limit') || '0')
  };

  if (response.status === 429) {
    const retryAfter = response.headers.get('Retry-After');
    throw new Error(`Rate limited. Retry after ${retryAfter} seconds`);
  }

  return { response, rateLimitInfo };
};

// Rate limit aware hook
export const useRateLimitedAPI = () => {
  const [rateLimitInfo, setRateLimitInfo] = useState<RateLimitInfo | null>(null);

  const callAPI = async (url: string, options: RequestInit) => {
    const { response, rateLimitInfo: newRateLimit } = await makeAPICall(url, options);
    setRateLimitInfo(newRateLimit);
    return response;
  };

  return { callAPI, rateLimitInfo };
};
```

## Best Practices

### 1. Environment Configuration

```typescript
// lib/config.ts
export const API_CONFIG = {
  baseURL: process.env.NEXT_PUBLIC_ASTROLOGY_API_URL || 'http://localhost:5000',
  apiKey: process.env.ASTROLOGY_API_KEY, // Server-side only
  timeout: 30000, // 30 seconds
  retries: 3
};

// Validate required environment variables
if (!API_CONFIG.baseURL) {
  throw new Error('NEXT_PUBLIC_ASTROLOGY_API_URL is required');
}

if (typeof window === 'undefined' && !API_CONFIG.apiKey) {
  console.warn('ASTROLOGY_API_KEY not found - API calls may fail');
}
```

### 2. API Client Class

```typescript
// lib/astrologyAPI.ts
class AstrologyAPI {
  private baseURL: string;
  private apiKey?: string;

  constructor(baseURL: string, apiKey?: string) {
    this.baseURL = baseURL;
    this.apiKey = apiKey;
  }

  private async makeRequest(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(url, {
      ...options,
      headers
    });

    return handleAPIResponse(response);
  }

  async calculateChart(data: ChartRequest): Promise<ChartResponse> {
    return this.makeRequest('/chart', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async getAyanamshaOptions() {
    return this.makeRequest('/ayanamsha-options');
  }

  async getSecurityStatus() {
    return this.makeRequest('/security-status');
  }
}

// Export configured instance
export const astrologyAPI = new AstrologyAPI(
  API_CONFIG.baseURL,
  API_CONFIG.apiKey
);
```

### 3. Caching Strategy

```typescript
// lib/cache.ts
import { NextRequest, NextResponse } from 'next/server';

const CACHE_DURATION = {
  chart: 24 * 60 * 60, // 24 hours
  ayanamsha: 7 * 24 * 60 * 60, // 7 days
  security: 5 * 60 // 5 minutes
};

export function withCache(handler: Function, duration: number) {
  return async (request: NextRequest) => {
    const response = await handler(request);
    
    if (response.ok) {
      // Add cache headers
      response.headers.set(
        'Cache-Control',
        `public, s-maxage=${duration}, stale-while-revalidate=86400`
      );
    }
    
    return response;
  };
}

// Usage in API routes
export const POST = withCache(async (request: NextRequest) => {
  // Your chart calculation logic
}, CACHE_DURATION.chart);
```

### 4. Type Safety with Zod

```typescript
// lib/schemas.ts
import { z } from 'zod';

export const ChartRequestSchema = z.object({
  year: z.number().int().min(1).max(9999),
  month: z.number().int().min(1).max(12),
  day: z.number().int().min(1).max(31),
  hour: z.number().int().min(0).max(23),
  minute: z.number().int().min(0).max(59).default(0),
  second: z.number().int().min(0).max(59).default(0),
  lat: z.number().min(-90).max(90),
  lon: z.number().min(-180).max(180),
  tz: z.string().default('UTC'),
  ayanamsha: z.string().default('lahiri'),
  house_system: z.string().default('placidus'),
  natal_ayanamsha: z.string().optional(),
  natal_house_system: z.string().optional(),
  transit_ayanamsha: z.string().optional(),
  transit_house_system: z.string().optional()
});

export type ChartRequest = z.infer<typeof ChartRequestSchema>;

// Validation helper
export const validateChartRequest = (data: unknown): ChartRequest => {
  return ChartRequestSchema.parse(data);
};
```

## Troubleshooting

### Common Issues and Solutions

#### 1. CORS Errors
```typescript
// If using domain authorization, ensure your domain is registered
// Check console for CORS-related errors
// Verify Origin header matches authorized domain
```

#### 2. Authentication Failures
```typescript
// Verify API key format and validity
// Check environment variables are loaded correctly
// Ensure Authorization header format: "Bearer YOUR_API_KEY"
```

#### 3. Rate Limiting
```typescript
// Implement exponential backoff for rate limited requests
const retryWithBackoff = async (fn: Function, maxRetries: number = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.statusCode === 429 && i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000; // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
};
```

#### 4. Invalid Date/Time Parameters
```typescript
// Validate date parameters before sending
const validateDateTime = (data: ChartRequest) => {
  const date = new Date(data.year, data.month - 1, data.day, data.hour, data.minute);
  
  if (isNaN(date.getTime())) {
    throw new Error('Invalid date/time parameters');
  }
  
  return data;
};
```

### Debug Mode

```typescript
// Enable debug logging in development
const DEBUG = process.env.NODE_ENV === 'development';

const debugLog = (message: string, data?: any) => {
  if (DEBUG) {
    console.log(`[Astrology API Debug] ${message}`, data);
  }
};

// Use in API calls
const response = await fetch(url, options);
debugLog('API Response', {
  status: response.status,
  headers: Object.fromEntries(response.headers.entries())
});
```

---

## Conclusion

This guide provides comprehensive patterns for integrating the Vedic Astrology Calculator API with Next.js applications. Choose the appropriate authentication method and integration pattern based on your specific use case:

- **Server-side API routes**: For secure API key usage
- **Client-side integration**: For public domain-authorized access
- **Server components**: For SSR and better SEO

Remember to implement proper error handling, respect rate limits, and follow security best practices when deploying to production.

For additional support or advanced usage patterns, refer to the API documentation or contact the development team.