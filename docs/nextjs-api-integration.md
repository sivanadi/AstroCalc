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
// Returns: { options: { "lahiri": { id: 1, name: "N.C. Lahiri" }, ... } }
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
  'Ketu': 'Ketu (South Node)' // Auto-calculated as opposite of Rahu
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
    'Authorization': `Bearer ${API_KEY}` // If using API key auth
    // Domain auth is handled automatically by the server based on request origin
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
// Returns: { options: { "lahiri": { id: 1, name: "N.C. Lahiri" }, ... } }
```

#### GET `/security-status`
Get API security configuration:
```typescript
const response = await fetch(`${API_BASE_URL}/security-status`);
const data = await response.json();
// Returns: { status: "secure", environment_auth: boolean, active_sessions: number, ... }
```

#### GET `/health`
API health check:
```typescript
const response = await fetch(`${API_BASE_URL}/health`);
const data = await response.json();
// Returns: { status: "healthy", ephe_path: "/path/to/ephemeris" }
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

// Chart Response (Actual structure from API)
interface ChartResponse {
  other_details: {
    natal_date_formatted: string;
    transit_date_formatted: string;
    natal_ayanamsha_name: string;
    transit_ayanamsha_name: string;
    ayanamsha_value_natal: number;
    ayanamsha_value_transit: number;
    natal_house_system_used: string;
    transit_house_system_used: string;
    timezone_used: string;
    natal_input_time_ut: string;
    transit_input_time_ut: string;
  };
  natal_planets: {
    [planetName: string]: number; // Longitude in degrees (e.g., "Sun": 54.12)
  };
  natal_house_cusps: {
    [houseName: string]: number; // House cusp in degrees (e.g., "House 1": 123.45)
  };
  transit_planets: {
    [planetName: string]: number; // Current planetary positions
  };
  transit_house_cusps: {
    [houseName: string]: number;
  };
}

// Error Response (FastAPI standard format)
interface ApiError {
  detail: string; // Error message
}

// Admin Models (for admin panel integration)
interface AdminLogin {
  username: string;
  password: string;
}

// For creating API keys
interface CreateAPIKeyRequest {
  name: string;
  description?: string; // Default: ''
  per_minute_limit?: number; // Default: 60
  per_day_limit?: number; // Default: 1000
  per_month_limit?: number; // Default: 30000
}

// For creating domains
interface CreateDomainRequest {
  domain: string;
  per_minute_limit?: number; // Default: 10
  per_day_limit?: number; // Default: 100
  per_month_limit?: number; // Default: 3000
}
```

## Complete API Access Methods Guide

### Method 1: GET Requests with Query Parameters

Both server-side and client-side applications can use GET requests with URL parameters:

```typescript
// Server-side (with API Key)
const buildChartURL = (params: ChartRequest) => {
  const url = new URL(`${API_BASE_URL}/chart`);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined) url.searchParams.set(key, value.toString());
  });
  return url.toString();
};

// Usage in Server Component with API Key
const chartData = await fetch(buildChartURL(chartParams), {
  headers: {
    'Authorization': `Bearer ${process.env.ASTROLOGY_API_KEY}`
  }
});

// Client-side (Domain Authorized)
const response = await fetch(buildChartURL(chartParams));
const data = await response.json();
```

### Method 2: POST Requests with JSON Body

For complex requests with structured data:

```typescript
// Server-side with API Key
const response = await fetch(`${API_BASE_URL}/chart`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`
  },
  body: JSON.stringify(chartData)
});

// Client-side (Domain Authorized)
const response = await fetch(`${API_BASE_URL}/chart`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
    // No Authorization header needed for domain-authorized requests
  },
  body: JSON.stringify(chartData)
});
```

### Method 3: Domain Authorization (Client-Side Friendly)

When your domain is pre-authorized by the API administrator, you can make direct client-side requests without API keys:

#### Setting Up Domain Authorization

1. **Contact API Administrator**: Request your domain to be added to the authorized domains list
2. **Configure Rate Limits**: Set appropriate limits for your domain's usage
3. **Verify Setup**: Test that requests from your domain work without API keys

#### Client-Side Implementation

```typescript
// hooks/useAstrologyAPI.ts
'use client'

import { useState, useCallback } from 'react';

interface DomainAuthorizedAPI {
  calculateChart: (data: ChartRequest, method?: 'GET' | 'POST') => Promise<ChartResponse>;
  getAyanamshaOptions: () => Promise<{ options: Record<string, { id: number; name: string }> }>;
  checkHealth: () => Promise<{ status: string; ephe_path: string }>;
}

export const useAstrologyAPI = (): DomainAuthorizedAPI => {
  const API_BASE_URL = process.env.NEXT_PUBLIC_ASTROLOGY_API_URL;

  const calculateChart = useCallback(async (data: ChartRequest, method: 'GET' | 'POST' = 'POST'): Promise<ChartResponse> => {
    if (!API_BASE_URL) {
      throw new Error('NEXT_PUBLIC_ASTROLOGY_API_URL environment variable is required for client-side requests');
    }

    let response: Response;

    if (method === 'GET') {
      // GET with query parameters
      const getUrl = new URL(`${API_BASE_URL}/chart`);
      Object.entries(data).forEach(([key, value]) => {
        if (value !== undefined) getUrl.searchParams.set(key, value.toString());
      });
      response = await fetch(getUrl.toString());
    } else {
      // POST with JSON body (default)
      response = await fetch(`${API_BASE_URL}/chart`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });
    }
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP ${response.status}: Request failed`);
    }

    return response.json();
  }, [API_BASE_URL]);

  const getAyanamshaOptions = useCallback(async (): Promise<{ options: Record<string, { id: number; name: string }> }> => {
    if (!API_BASE_URL) {
      throw new Error('NEXT_PUBLIC_ASTROLOGY_API_URL environment variable is required');
    }

    const response = await fetch(`${API_BASE_URL}/ayanamsha-options`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch ayanamsha options: ${response.status}`);
    }

    return response.json();
  }, [API_BASE_URL]);

  const checkHealth = useCallback(async (): Promise<{ status: string; ephe_path: string }> => {
    if (!API_BASE_URL) {
      throw new Error('NEXT_PUBLIC_ASTROLOGY_API_URL environment variable is required');
    }

    const response = await fetch(`${API_BASE_URL}/health`);
    
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return response.json();
  }, [API_BASE_URL]);

  return {
    calculateChart,
    getAyanamshaOptions,
    checkHealth
  };
};
```

#### Client Component Example

```typescript
// components/DomainAuthorizedChart.tsx
'use client'

import { useState } from 'react';
import { useAstrologyAPI } from '@/hooks/useAstrologyAPI';

export function DomainAuthorizedChart() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ChartResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { calculateChart } = useAstrologyAPI();

  const handleCalculate = async (formData: FormData) => {
    setLoading(true);
    setError(null);

    try {
      const chartRequest: ChartRequest = {
        year: parseInt(formData.get('year') as string),
        month: parseInt(formData.get('month') as string),
        day: parseInt(formData.get('day') as string),
        hour: parseInt(formData.get('hour') as string),
        minute: parseInt(formData.get('minute') as string) || 0,
        lat: parseFloat(formData.get('lat') as string),
        lon: parseFloat(formData.get('lon') as string),
        tz: formData.get('tz') as string || 'UTC',
        ayanamsha: formData.get('ayanamsha') as string || 'lahiri',
        house_system: formData.get('house_system') as string || 'placidus'
      };

      const chartData = await calculateChart(chartRequest);
      setResult(chartData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Domain Authorized Chart Calculator</h2>
      
      <form onSubmit={(e) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        handleCalculate(formData);
      }} className="space-y-4">
        {/* Form fields... */}
        <div className="grid grid-cols-2 gap-4">
          <input name="year" type="number" placeholder="Year" required />
          <input name="month" type="number" placeholder="Month" min="1" max="12" required />
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          <input name="day" type="number" placeholder="Day" min="1" max="31" required />
          <input name="hour" type="number" placeholder="Hour" min="0" max="23" required />
          <input name="minute" type="number" placeholder="Minute" min="0" max="59" defaultValue="0" />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <input name="lat" type="number" step="any" placeholder="Latitude" required />
          <input name="lon" type="number" step="any" placeholder="Longitude" required />
        </div>

        <select name="tz" defaultValue="UTC">
          <option value="UTC">UTC</option>
          <option value="Asia/Kolkata">Asia/Kolkata</option>
          <option value="America/New_York">America/New_York</option>
        </select>

        <button 
          type="submit" 
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded disabled:opacity-50"
        >
          {loading ? 'Calculating...' : 'Calculate Chart (Domain Authorized)'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          Error: {error}
        </div>
      )}

      {result && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-4">Chart Results</h3>
          <div className="bg-gray-100 p-4 rounded">
            <p>Date: {result.other_details.natal_date_formatted}</p>
            <p>Ayanamsha: {result.other_details.natal_ayanamsha_name}</p>
            <div className="mt-4">
              <h4 className="font-medium">Planetary Positions:</h4>
              <div className="grid grid-cols-2 gap-2 mt-2">
                {Object.entries(result.natal_planets).map(([planet, longitude]) => (
                  <div key={planet}>
                    <strong>{planet}:</strong> {longitude.toFixed(2)}°
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

## Next.js Integration Patterns

### 1. Server Actions (Next.js 15 - Recommended for Forms)

Server Actions provide a secure, server-side way to handle form submissions and mutations without creating separate API routes.

#### Basic Server Action Implementation
```typescript
// actions/chart-actions.ts
'use server'

import { auth } from '@/auth' // Your auth method
import { redirect } from 'next/navigation'
import { revalidatePath } from 'next/cache'
import { z } from 'zod'

const ChartRequestSchema = z.object({
  year: z.number().int().min(1).max(9999),
  month: z.number().int().min(1).max(12),
  day: z.number().int().min(1).max(31),
  hour: z.number().int().min(0).max(23),
  minute: z.number().int().min(0).max(59).default(0),
  lat: z.number().min(-90).max(90),
  lon: z.number().min(-180).max(180),
  tz: z.string().default('UTC'),
  ayanamsha: z.string().default('lahiri'),
  house_system: z.string().default('placidus')
})

const API_BASE_URL = process.env.ASTROLOGY_API_URL
const API_KEY = process.env.ASTROLOGY_API_KEY

export async function calculateChartAction(prevState: any, formData: FormData) {
  // 1. Environment configuration check
  if (!API_BASE_URL || !API_KEY) {
    console.error('API configuration missing: ASTROLOGY_API_URL and ASTROLOGY_API_KEY must be set')
    return { 
      success: false, 
      error: 'API configuration error. Please contact support.' 
    }
  }

  // 2. Authentication check (if required)
  const session = await auth?.() // Uncomment if authentication needed
  // if (!session?.user) {
  //   return { success: false, error: 'Authentication required' }
  // }

  // 3. Input validation
  const rawData = {
    year: parseInt(formData.get('year') as string),
    month: parseInt(formData.get('month') as string),
    day: parseInt(formData.get('day') as string),
    hour: parseInt(formData.get('hour') as string),
    minute: parseInt(formData.get('minute') as string) || 0,
    lat: parseFloat(formData.get('lat') as string),
    lon: parseFloat(formData.get('lon') as string),
    tz: formData.get('tz') as string || 'UTC',
    ayanamsha: formData.get('ayanamsha') as string || 'lahiri',
    house_system: formData.get('house_system') as string || 'placidus'
  }

  let validatedData
  try {
    validatedData = ChartRequestSchema.parse(rawData)
  } catch (error) {
    return { 
      success: false, 
      error: `Invalid form data: ${error instanceof Error ? error.message : 'Validation failed'}` 
    }
  }

  // 4. API call to astrology service
  try {
    const response = await fetch(`${API_BASE_URL}/chart`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify(validatedData)
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'API request failed' }))
      return { 
        success: false, 
        error: error.detail || `HTTP ${response.status}: Chart calculation failed` 
      }
    }

    const chartData = await response.json()
    
    // 5. Optionally save to database
    // await saveChartToDatabase(chartData, session?.user?.id)
    
    // 6. Revalidate cached data if needed
    revalidatePath('/charts')
    
    return { success: true, data: chartData }
  } catch (error) {
    console.error('Chart calculation error:', error)
    return { 
      success: false, 
      error: 'Failed to calculate chart. Please check your connection and try again.' 
    }
  }
}

export async function saveChartAction(prevState: any, formData: FormData) {
  const session = await auth?.()
  if (!session?.user?.id) {
    return { 
      success: false, 
      error: 'Authentication required to save charts' 
    }
  }

  try {
    const chartDataString = formData.get('chartData') as string
    const name = formData.get('name') as string

    if (!chartDataString || !name) {
      return { 
        success: false, 
        error: 'Chart data and name are required' 
      }
    }

    const chartData = JSON.parse(chartDataString)

    // Save chart to database with user association
    // await db.chart.create({
    //   data: {
    //     name,
    //     data: chartData,
    //     userId: session.user.id
    //   }
    // })

    revalidatePath('/my-charts')
    return { success: true, message: 'Chart saved successfully' }
  } catch (error) {
    console.error('Save chart error:', error)
    return { 
      success: false, 
      error: 'Failed to save chart. Please try again.' 
    }
  }
}
```

#### Using Server Actions in Components
```typescript
// components/ChartForm.tsx
'use client'

import { calculateChartAction } from '@/actions/chart-actions'
import { useFormStatus } from 'react-dom'
import { useActionState } from 'react'

function SubmitButton() {
  const { pending } = useFormStatus()
  
  return (
    <button 
      type="submit" 
      disabled={pending}
      className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
    >
      {pending ? 'Calculating...' : 'Calculate Chart'}
    </button>
  )
}

export function ChartForm() {
  const [state, formAction] = useActionState(calculateChartAction, null)

  return (
    <form action={formAction} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <input
          name="year"
          type="number"
          placeholder="Year"
          required
          className="px-3 py-2 border rounded"
        />
        <input
          name="month"
          type="number"
          placeholder="Month (1-12)"
          min="1"
          max="12"
          required
          className="px-3 py-2 border rounded"
        />
      </div>
      
      <div className="grid grid-cols-3 gap-4">
        <input
          name="day"
          type="number"
          placeholder="Day"
          min="1"
          max="31"
          required
          className="px-3 py-2 border rounded"
        />
        <input
          name="hour"
          type="number"
          placeholder="Hour (0-23)"
          min="0"
          max="23"
          required
          className="px-3 py-2 border rounded"
        />
        <input
          name="minute"
          type="number"
          placeholder="Minute (0-59)"
          min="0"
          max="59"
          defaultValue="0"
          className="px-3 py-2 border rounded"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <input
          name="lat"
          type="number"
          step="any"
          placeholder="Latitude"
          required
          className="px-3 py-2 border rounded"
        />
        <input
          name="lon"
          type="number"
          step="any"
          placeholder="Longitude"
          required
          className="px-3 py-2 border rounded"
        />
      </div>

      <select
        name="tz"
        defaultValue="UTC"
        className="w-full px-3 py-2 border rounded"
      >
        <option value="UTC">UTC</option>
        <option value="Asia/Kolkata">Asia/Kolkata</option>
        <option value="America/New_York">America/New_York</option>
        <option value="Europe/London">Europe/London</option>
      </select>

      <SubmitButton />

      {state?.success && (
        <div className="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          Chart calculated successfully!
          {state.data && (
            <div className="mt-2">
              <p>Date: {state.data.other_details?.natal_date_formatted}</p>
              <p>Ayanamsha: {state.data.other_details?.natal_ayanamsha_name}</p>
            </div>
          )}
        </div>
      )}

      {state?.success === false && state?.error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          Error: {state.error}
        </div>
      )}
    </form>
  )
}
```

### 2. Server-Side Rendering (SSR) with API Routes

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
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  // Environment configuration check
  if (!API_BASE_URL || !API_KEY) {
    console.error('API configuration missing: ASTROLOGY_API_URL and ASTROLOGY_API_KEY must be set');
    return res.status(500).json({ 
      detail: 'API configuration error. ASTROLOGY_API_URL and ASTROLOGY_API_KEY environment variables must be configured.' 
    });
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
      const error = await response.json().catch(() => ({ detail: 'API request failed' }));
      return res.status(response.status).json({ detail: error.detail || `HTTP ${response.status}: Request failed` });
    }

    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    console.error('API Error:', error);
    res.status(500).json({ detail: 'Internal server error' });
  }
}
```

#### app/api/chart/route.ts (App Router)
```typescript
import { NextRequest, NextResponse } from 'next/server';

const API_BASE_URL = process.env.ASTROLOGY_API_URL;
const API_KEY = process.env.ASTROLOGY_API_KEY;

export async function POST(request: NextRequest) {
  // Environment configuration check
  if (!API_BASE_URL || !API_KEY) {
    console.error('API configuration missing: ASTROLOGY_API_URL and ASTROLOGY_API_KEY must be set');
    return NextResponse.json(
      { detail: 'API configuration error. ASTROLOGY_API_URL and ASTROLOGY_API_KEY environment variables must be configured.' },
      { status: 500 }
    );
  }

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
      const error = await response.json().catch(() => ({ detail: 'API request failed' }));
      return NextResponse.json(
        { detail: error.detail || `HTTP ${response.status}: Request failed` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### 3. Client-Side Integration

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
        const errorData = await response.json().catch(() => ({ detail: 'Request failed' }));
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
                {Object.entries(chartData.natal_planets).map(([planet, longitude]) => (
                  <div key={planet} className="flex justify-between">
                    <span className="capitalize">{planet}:</span>
                    <span>{longitude.toFixed(2)}°</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-medium mb-2">House Cusps</h4>
              <div className="space-y-2">
                {Object.entries(chartData.natal_house_cusps).map(([house, cusp]) => (
                  <div key={house} className="flex justify-between">
                    <span>{house}:</span>
                    <span>{cusp.toFixed(2)}°</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <div className="mt-4 p-4 bg-gray-100 rounded">
            <h4 className="font-medium mb-2">Chart Details</h4>
            <p>Ayanamsha: {chartData.other_details.natal_ayanamsha_name}</p>
            <p>House System: {chartData.other_details.natal_house_system_used}</p>
            <p>Date: {chartData.other_details.natal_date_formatted}</p>
          </div>
        </div>
      )}
    </div>
  );
}
```

### 4. Server Component Integration (App Router)

```typescript
// app/chart/[id]/page.tsx
import { ChartDisplay } from '@/components/ChartDisplay';
import { notFound } from 'next/navigation';
import { cache } from 'react';

// Cache the chart data function to avoid duplicate requests
const getChartData = cache(async (chartId: string) => {
  const API_BASE_URL = process.env.ASTROLOGY_API_URL;
  const API_KEY = process.env.ASTROLOGY_API_KEY;

  if (!API_BASE_URL || !API_KEY) {
    throw new Error('API configuration missing');
  }

  // Example: Get saved chart data and calculate
  const chartParams = await getSavedChartParams(chartId);
  
  if (!chartParams) {
    notFound();
  }
  
  const response = await fetch(`${API_BASE_URL}/chart`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`
    },
    body: JSON.stringify(chartParams),
    // Modern caching strategy
    next: { 
      revalidate: 3600, // Cache for 1 hour
      tags: [`chart-${chartId}`] // Enable selective revalidation
    }
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP ${response.status}: Failed to fetch chart data`);
  }

  return response.json();
});

export default async function ChartPage({ params }: { params: { id: string } }) {
  const chartData = await getChartData(params.id);

  return (
    <div>
      <h1>Vedic Chart Analysis</h1>
      <ChartDisplay data={chartData} />
    </div>
  );
}

// Generate metadata for SEO
export async function generateMetadata({ params }: { params: { id: string } }) {
  try {
    const chartData = await getChartData(params.id);
    
    return {
      title: `Vedic Chart Analysis - ${chartData.other_details?.natal_date_formatted || 'Unknown Date'}`,
      description: `Detailed Vedic astrology chart analysis using ${chartData.other_details?.natal_ayanamsha_name || 'Lahiri'} ayanamsha`
    };
  } catch (error) {
    return {
      title: 'Vedic Chart Analysis',
      description: 'Professional Vedic astrology chart analysis'
    };
  }
}
```

### 5. Advanced Caching and Performance Optimization (Next.js 15)

#### Intelligent Cache Management
```typescript
// lib/cache-manager.ts
import { revalidateTag } from 'next/cache';
import { cache } from 'react';

export class ChartCacheManager {
  static async invalidateUserCharts(userId: string) {
    revalidateTag(`user-charts-${userId}`);
  }
  
  static async invalidateChart(chartId: string) {
    revalidateTag(`chart-${chartId}`);
  }
  
  static async invalidateAyanamshaData() {
    revalidateTag('ayanamsha-options');
  }
}

// Enhanced data fetcher with cache tags and environment guards
export const fetchWithCache = cache(async (
  url: string, 
  options: RequestInit = {},
  cacheConfig: { revalidate?: number; tags?: string[] } = {}
) => {
  const API_BASE_URL = process.env.ASTROLOGY_API_URL;
  const API_KEY = process.env.ASTROLOGY_API_KEY;
  
  if (!API_BASE_URL || !API_KEY) {
    throw new Error('ASTROLOGY_API_URL and ASTROLOGY_API_KEY environment variables must be configured');
  }
  
  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`,
      ...options.headers
    },
    next: {
      revalidate: cacheConfig.revalidate || 3600,
      tags: cacheConfig.tags || []
    }
  });
  
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} - ${response.statusText}`);
  }
  
  return response.json();
});

// Usage in Server Components
export async function getAyanamshaOptions() {
  return fetchWithCache('/ayanamsha-options', {}, {
    revalidate: 7 * 24 * 60 * 60, // 7 days
    tags: ['ayanamsha-options']
  });
}

// Note: This would be for a user-specific charts endpoint if your API supports it
// Currently the Vedic Astrology API doesn't have user management, so this is a placeholder
export async function getUserCharts() {
  // This would typically require authentication and a user-specific endpoint
  // Since the current API doesn't have user management, this is a conceptual example
  throw new Error('User charts endpoint not implemented in current API');
}
```

#### Streaming and Suspense Patterns
```typescript
// app/dashboard/page.tsx
import { Suspense } from 'react';
import { UserCharts } from '@/components/UserCharts';
import { RecentActivity } from '@/components/RecentActivity';
import { ChartsSkeleton, ActivitySkeleton } from '@/components/Skeletons';

export default function DashboardPage() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Suspense fallback={<ChartsSkeleton />}>
        <UserCharts />
      </Suspense>
      
      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity />
      </Suspense>
    </div>
  );
}

// components/UserCharts.tsx
async function UserCharts() {
  // Since the current API doesn't have user management, 
  // this would typically fetch from your own database of saved charts
  try {
    // Example: const charts = await db.charts.findMany({ where: { userId } });
    const mockCharts = []; // Replace with actual database query
    
    return (
      <div>
        <h2>Your Charts</h2>
        {mockCharts.length > 0 ? (
          mockCharts.map(chart => (
            <ChartCard key={chart.id} chart={chart} />
          ))
        ) : (
          <p>No saved charts yet. Calculate your first chart!</p>
        )}
      </div>
    );
  } catch (error) {
    console.error('Failed to load charts:', error);
    return (
      <div>
        <h2>Your Charts</h2>
        <p>Unable to load charts. Please try again later.</p>
      </div>
    );
  }
}
```

### 6. Enhanced Security Patterns (2024)

#### CSRF Protection for Server Actions
```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: {
      // Enable CSRF protection
      allowedOrigins: [
        'localhost:3000',
        'yourdomain.com',
        'www.yourdomain.com'
      ]
    }
  }
}

module.exports = nextConfig
```

#### Rate Limiting for API Routes
```typescript
// lib/rate-limiter.ts
import { NextRequest } from 'next/server';

interface RateLimitConfig {
  requests: number;
  window: number; // in seconds
}

class RateLimiter {
  private cache = new Map<string, { count: number; resetTime: number }>();

  async check(request: NextRequest, config: RateLimitConfig): Promise<boolean> {
    const identifier = this.getIdentifier(request);
    const now = Date.now();
    
    const record = this.cache.get(identifier);
    
    if (!record || now > record.resetTime) {
      this.cache.set(identifier, {
        count: 1,
        resetTime: now + (config.window * 1000)
      });
      return true;
    }
    
    if (record.count >= config.requests) {
      return false; // Rate limited
    }
    
    record.count++;
    return true;
  }
  
  private getIdentifier(request: NextRequest): string {
    // Use IP address or authenticated user ID
    const forwarded = request.headers.get('x-forwarded-for');
    const ip = forwarded ? forwarded.split(',')[0] : request.ip;
    return ip || 'unknown';
  }
}

export const rateLimiter = new RateLimiter();

// Usage in API routes
export async function POST(request: NextRequest) {
  const isAllowed = await rateLimiter.check(request, {
    requests: 10, // 10 requests
    window: 60    // per minute
  });
  
  if (!isAllowed) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429 }
    );
  }
  
  // Continue with request processing...
}
```

#### Input Sanitization and Validation
```typescript
// lib/validation.ts
import { z } from 'zod';
import DOMPurify from 'isomorphic-dompurify';

export const sanitizeInput = (input: string): string => {
  return DOMPurify.sanitize(input, { 
    ALLOWED_TAGS: [], 
    ALLOWED_ATTR: [] 
  });
};

export const ChartRequestSchema = z.object({
  year: z.number().int().min(1).max(9999),
  month: z.number().int().min(1).max(12),
  day: z.number().int().min(1).max(31),
  hour: z.number().int().min(0).max(23),
  minute: z.number().int().min(0).max(59).default(0),
  second: z.number().int().min(0).max(59).default(0),
  lat: z.number().min(-90).max(90),
  lon: z.number().min(-180).max(180),
  tz: z.string().min(1).max(50).refine(
    (tz) => {
      // Validate timezone string
      try {
        Intl.DateTimeFormat(undefined, { timeZone: tz });
        return true;
      } catch {
        return false;
      }
    },
    { message: 'Invalid timezone' }
  ),
  ayanamsha: z.string().min(1).max(50),
  house_system: z.string().min(1).max(20),
  // Optional fields with validation
  natal_ayanamsha: z.string().min(1).max(50).optional(),
  natal_house_system: z.string().min(1).max(20).optional(),
  transit_ayanamsha: z.string().min(1).max(50).optional(),
  transit_house_system: z.string().min(1).max(20).optional()
}).refine((data) => {
  // Validate date is not in the future beyond reasonable limits
  const inputDate = new Date(data.year, data.month - 1, data.day);
  const maxFutureDate = new Date();
  maxFutureDate.setFullYear(maxFutureDate.getFullYear() + 100);
  
  return inputDate <= maxFutureDate;
}, { message: 'Date cannot be more than 100 years in the future' });

// Sanitize and validate function
export function sanitizeAndValidateChartRequest(rawData: unknown): z.infer<typeof ChartRequestSchema> {
  // First sanitize string inputs if they exist
  if (typeof rawData === 'object' && rawData !== null) {
    const sanitized = { ...rawData as any };
    
    if (typeof sanitized.tz === 'string') {
      sanitized.tz = sanitizeInput(sanitized.tz);
    }
    if (typeof sanitized.ayanamsha === 'string') {
      sanitized.ayanamsha = sanitizeInput(sanitized.ayanamsha);
    }
    if (typeof sanitized.house_system === 'string') {
      sanitized.house_system = sanitizeInput(sanitized.house_system);
    }
    
    return ChartRequestSchema.parse(sanitized);
  }
  
  return ChartRequestSchema.parse(rawData);
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

## Environment Setup

### Required Environment Variables

Before using any of the integration patterns, you must configure these environment variables:

```bash
# .env.local (for development) or deployment environment
ASTROLOGY_API_URL=https://your-api-domain.com
ASTROLOGY_API_KEY=your_secure_api_key_here
```

⚠️ **Critical**: All code examples in this guide will fail with silent errors if these variables are not set. The enhanced examples include proper error handling to detect missing configuration.

### Getting Your API Key

1. **Contact the API administrator** to get your API key
2. **Set your domain authorization** (if using client-side requests)
3. **Configure rate limits** appropriate for your application's needs

### Testing Your Configuration

```typescript
// lib/config-test.ts
export function validateAPIConfig() {
  const apiUrl = process.env.ASTROLOGY_API_URL;
  const apiKey = process.env.ASTROLOGY_API_KEY;
  
  if (!apiUrl) {
    throw new Error('ASTROLOGY_API_URL environment variable is required');
  }
  
  if (!apiKey) {
    throw new Error('ASTROLOGY_API_KEY environment variable is required');
  }
  
  console.log('✅ API configuration is valid');
  return { apiUrl, apiKey };
}

// Call this in your application startup
try {
  validateAPIConfig();
} catch (error) {
  console.error('❌ API Configuration Error:', error.message);
  process.exit(1);
}
```

## Production Deployment Checklist

### Environment Configuration
```bash
# Required environment variables for production
ASTROLOGY_API_URL=https://your-api-domain.com
ASTROLOGY_API_KEY=your_secure_api_key_here

# Optional configuration
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1

# For authentication (if using NextAuth.js)
NEXTAUTH_URL=https://your-nextjs-app.com
NEXTAUTH_SECRET=your_nextauth_secret_here
```

### Next.js 15 Production Configuration
```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Security enhancements
  experimental: {
    serverActions: {
      allowedOrigins: [
        process.env.NEXTAUTH_URL,
        'yourdomain.com'
      ]
    }
  },
  
  // Performance optimizations
  images: {
    formats: ['image/webp', 'image/avif'],
  },
  
  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin'
          }
        ]
      }
    ];
  }
}

module.exports = nextConfig
```

### Performance Monitoring
```typescript
// lib/analytics.ts
export function trackChartCalculation(duration: number, ayanamsha: string) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'chart_calculated', {
      event_category: 'astrology',
      event_label: ayanamsha,
      value: Math.round(duration)
    });
  }
}

export function trackAPIError(endpoint: string, errorCode: number) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'api_error', {
      event_category: 'api',
      event_label: endpoint,
      value: errorCode
    });
  }
}
```

## Conclusion

This comprehensive guide provides modern patterns for integrating the Vedic Astrology Calculator API with Next.js 15 applications, incorporating the latest 2024 best practices:

### Key Integration Approaches:
- **Server Actions** (Recommended): Modern form handling with built-in security
- **Server Components**: Optimal performance and SEO with intelligent caching
- **API Routes**: Traditional approach for custom authentication needs
- **Client-side integration**: For interactive components with real-time updates

### Security Features:
- ✅ CSRF protection for Server Actions
- ✅ Input validation and sanitization
- ✅ Rate limiting implementation
- ✅ Secure environment variable handling

### Performance Optimizations:
- ✅ Intelligent caching with cache tags
- ✅ Streaming and Suspense patterns
- ✅ Request deduplication with React cache
- ✅ Selective revalidation strategies

### Production Ready:
- ✅ Comprehensive error handling
- ✅ Type safety with Zod validation
- ✅ Analytics and monitoring
- ✅ Deployment best practices

Choose the appropriate pattern based on your specific requirements:
- **Public applications**: Use domain authorization with client-side integration
- **Authenticated applications**: Use Server Actions with API key authentication
- **High-performance needs**: Combine Server Components with intelligent caching
- **Complex forms**: Leverage Server Actions with real-time validation

For questions, advanced implementation guidance, or API support, refer to the main API documentation or contact the development team.