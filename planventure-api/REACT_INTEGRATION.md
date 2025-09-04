# React Frontend Integration Guide

## CORS Configuration

The Flask API is now configured to work with React frontends. Here's what's been set up:

### Backend CORS Settings

#### Allowed Origins:
- `http://localhost:3000` (Default React dev server)
- `http://127.0.0.1:3000` (Alternative localhost)
- `http://localhost:3001` (Alternative React port)
- `http://127.0.0.1:3001` (Alternative localhost)
- Production URL from `FRONTEND_URL` environment variable

#### Allowed Methods:
- `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`

#### Allowed Headers:
- `Content-Type`
- `Authorization`
- `X-Requested-With`
- `Access-Control-Allow-Credentials`

---

## React Frontend Setup

### 1. Install Axios for API calls:
```bash
npm install axios
```

### 2. Create API service file (`src/services/api.js`):

```javascript
import axios from 'axios';

// Base API URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Enable credentials for CORS
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### 3. Create authentication service (`src/services/auth.js`):

```javascript
import apiClient from './api';

export const authService = {
  // Register user
  register: async (email, password) => {
    try {
      const response = await apiClient.post('/api/auth/register', {
        email,
        password,
      });
      
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
      }
      
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Login user
  login: async (email, password) => {
    try {
      const response = await apiClient.post('/api/auth/login', {
        email,
        password,
      });
      
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
      }
      
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Logout user
  logout: async () => {
    try {
      await apiClient.post('/api/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  },

  // Get current user
  getCurrentUser: async () => {
    try {
      const response = await apiClient.get('/api/auth/me');
      return response.data.user;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },
};
```

### 4. Create trips service (`src/services/trips.js`):

```javascript
import apiClient from './api';

export const tripsService = {
  // Get all user trips
  getTrips: async () => {
    try {
      const response = await apiClient.get('/api/trips/');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Create new trip
  createTrip: async (tripData) => {
    try {
      const response = await apiClient.post('/api/trips/', tripData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get specific trip
  getTrip: async (tripId) => {
    try {
      const response = await apiClient.get(`/api/trips/${tripId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Update trip
  updateTrip: async (tripId, tripData) => {
    try {
      const response = await apiClient.put(`/api/trips/${tripId}`, tripData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Delete trip
  deleteTrip: async (tripId) => {
    try {
      const response = await apiClient.delete(`/api/trips/${tripId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get itinerary suggestions
  getItinerarySuggestions: async (destination, startDate, endDate) => {
    try {
      const response = await apiClient.post('/api/trips/itinerary-suggestions', {
        destination,
        start_date: startDate,
        end_date: endDate,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};
```

### 5. Environment Variables (`.env`):

```env
REACT_APP_API_URL=http://127.0.0.1:5000
```

### 6. Example React Component (`src/components/TripList.js`):

```javascript
import React, { useState, useEffect } from 'react';
import { tripsService } from '../services/trips';

const TripList = () => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTrips();
  }, []);

  const fetchTrips = async () => {
    try {
      setLoading(true);
      const data = await tripsService.getTrips();
      setTrips(data.trips);
    } catch (error) {
      setError(error.message || 'Failed to fetch trips');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading trips...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>My Trips ({trips.length})</h2>
      {trips.map((trip) => (
        <div key={trip.id} style={{ border: '1px solid #ccc', margin: '10px', padding: '10px' }}>
          <h3>{trip.destination}</h3>
          <p>
            {trip.start_date} to {trip.end_date}
          </p>
          {trip.coordinates && (
            <p>
              Coordinates: {trip.coordinates.latitude}, {trip.coordinates.longitude}
            </p>
          )}
          <details>
            <summary>Itinerary</summary>
            <pre>{trip.itinerary}</pre>
          </details>
        </div>
      ))}
    </div>
  );
};

export default TripList;
```

---

## Testing CORS

### 1. Test CORS endpoint:
```bash
curl --location 'http://127.0.0.1:5000/cors-test' \
--header 'Origin: http://localhost:3000'
```

### 2. Test from React:
```javascript
// In your React component or service
fetch('http://127.0.0.1:5000/cors-test', {
  method: 'GET',
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
  },
})
.then(response => response.json())
.then(data => console.log('CORS test:', data));
```

---

## Production Deployment

### Backend Environment Variables:
```env
FRONTEND_URL=https://your-react-app.netlify.app
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret
```

### React Environment Variables:
```env
REACT_APP_API_URL=https://your-flask-api.herokuapp.com
```

The API is now fully configured to work with React frontends in both development and production environments! 🚀
