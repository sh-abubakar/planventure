# Trip Routes API Testing Examples

## Prerequisites
First, you need to register a user and get JWT tokens:

### 1. Register User
```bash
curl --location 'http://127.0.0.1:5000/api/auth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
  "email": "testuser@example.com",
  "password": "testpassword123"
}'
```

### 2. Login to Get Tokens
```bash
curl --location 'http://127.0.0.1:5000/api/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
  "email": "testuser@example.com",
  "password": "testpassword123"
}'
```

**Note:** Copy the `access_token` from the response and use it in the Authorization header below.

---

## Trip CRUD Operations

### 1. CREATE Trip - POST /api/trips/

#### Example 1: Basic Trip
```bash
curl --location 'http://127.0.0.1:5000/api/trips/' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN_HERE' \
--header 'Content-Type: application/json' \
--data-raw '{
  "destination": "Paris, France",
  "start_date": "2024-10-15",
  "end_date": "2024-10-22",
  "itinerary": "Day 1: Arrive and visit Eiffel Tower\nDay 2: Louvre Museum\nDay 3: Versailles Palace\nDay 4-7: Explore neighborhoods and cafes"
}'
```

#### Example 2: Trip with Coordinates
```bash
curl --location 'http://127.0.0.1:5000/api/trips/' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN_HERE' \
--header 'Content-Type: application/json' \
--data-raw '{
  "destination": "Tokyo, Japan",
  "start_date": "2024-11-01",
  "end_date": "2024-11-10",
  "latitude": 35.6762,
  "longitude": 139.6503,
  "itinerary": "Day 1-2: Shibuya and Harajuku\nDay 3-4: Traditional temples in Asakusa\nDay 5-6: Day trip to Mount Fuji\nDay 7-9: Osaka and Kyoto\nDay 10: Shopping in Ginza"
}'
```

#### Example 3: Weekend Getaway
```bash
curl --location 'http://127.0.0.1:5000/api/trips/' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN_HERE' \
--header 'Content-Type: application/json' \
--data-raw '{
  "destination": "New York City, USA",
  "start_date": "2024-12-14",
  "end_date": "2024-12-16",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "itinerary": "Friday: Arrive, Times Square, Broadway show\nSaturday: Central Park, Museums, Brooklyn Bridge\nSunday: Statue of Liberty, departure"
}'
```

### 2. READ All Trips - GET /api/trips/
```bash
curl --location 'http://127.0.0.1:5000/api/trips/' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN_HERE'
```

### 3. READ Specific Trip - GET /api/trips/{trip_id}
```bash
curl --location 'http://127.0.0.1:5000/api/trips/1' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN_HERE'
```

### 4. UPDATE Trip - PUT /api/trips/{trip_id}

#### Example 1: Update Destination and Dates
```bash
curl --location --request PUT 'http://127.0.0.1:5000/api/trips/1' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN_HERE' \
--header 'Content-Type: application/json' \
--data-raw '{
  "destination": "Paris & London, Europe",
  "start_date": "2024-10-15",
  "end_date": "2024-10-25"
}'
```

#### Example 2: Update Only Itinerary
```bash
curl --location --request PUT 'http://127.0.0.1:5000/api/trips/1' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN_HERE' \
--header 'Content-Type: application/json' \
--data-raw '{
  "itinerary": "Updated itinerary:\nDay 1-4: Paris - Eiffel Tower, Louvre, Seine River cruise\nDay 5-7: London - Big Ben, Tower Bridge, British Museum\nDay 8-10: Explore both cities, shopping, local cuisine"
}'
```

#### Example 3: Add/Update Coordinates
```bash
curl --location --request PUT 'http://127.0.0.1:5000/api/trips/2' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN_HERE' \
--header 'Content-Type: application/json' \
--data-raw '{
  "latitude": 35.6895,
  "longitude": 139.6917,
  "itinerary": "Updated Tokyo itinerary with specific coordinates for Shinjuku area"
}'
```

### 5. DELETE Trip - DELETE /api/trips/{trip_id}
```bash
curl --location --request DELETE 'http://127.0.0.1:5000/api/trips/1' \
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN_HERE'
```

---

## Test Data Variations

### Business Trip Example
```json
{
  "destination": "San Francisco, CA",
  "start_date": "2024-09-20",
  "end_date": "2024-09-23",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "itinerary": "Business conference at Moscone Center\nDay 1: Arrival, conference registration\nDay 2-3: Conference sessions and networking\nDay 4: Client meetings, departure"
}
```

### Family Vacation Example
```json
{
  "destination": "Orlando, Florida",
  "start_date": "2024-12-20",
  "end_date": "2024-12-27",
  "latitude": 28.5383,
  "longitude": -81.3792,
  "itinerary": "Family Disney World vacation\nDay 1: Magic Kingdom\nDay 2: EPCOT\nDay 3: Hollywood Studios\nDay 4: Animal Kingdom\nDay 5-6: Universal Studios\nDay 7: Rest and shopping, departure"
}
```

### Adventure Trip Example
```json
{
  "destination": "Reykjavik, Iceland",
  "start_date": "2024-08-10",
  "end_date": "2024-08-17",
  "latitude": 64.1466,
  "longitude": -21.9426,
  "itinerary": "Iceland adventure tour\nDay 1-2: Reykjavik city exploration\nDay 3: Golden Circle tour\nDay 4-5: South coast waterfalls and black beaches\nDay 6: Blue Lagoon and Northern Lights hunt\nDay 7: Departure"
}
```

### Error Testing Examples

#### Invalid Date Format
```json
{
  "destination": "Test Destination",
  "start_date": "2024/10/15",
  "end_date": "2024/10/22"
}
```

#### Start Date After End Date
```json
{
  "destination": "Test Destination",
  "start_date": "2024-10-22",
  "end_date": "2024-10-15"
}
```

#### Missing Required Fields
```json
{
  "destination": "Test Destination"
}
```

---

## Expected Response Formats

### Successful Trip Creation
```json
{
  "message": "Trip created successfully",
  "trip": {
    "id": 1,
    "user_id": 1,
    "destination": "Paris, France",
    "start_date": "2024-10-15",
    "end_date": "2024-10-22",
    "coordinates": {
      "latitude": 48.8566,
      "longitude": 2.3522
    },
    "itinerary": "Day 1: Arrive and visit Eiffel Tower...",
    "created_at": "2024-09-04T10:30:00",
    "updated_at": "2024-09-04T10:30:00"
  }
}
```

### Get All Trips Response
```json
{
  "trips": [
    {
      "id": 1,
      "user_id": 1,
      "destination": "Paris, France",
      "start_date": "2024-10-15",
      "end_date": "2024-10-22",
      "coordinates": {
        "latitude": 48.8566,
        "longitude": 2.3522
      },
      "itinerary": "Day 1: Arrive and visit Eiffel Tower...",
      "created_at": "2024-09-04T10:30:00",
      "updated_at": "2024-09-04T10:30:00"
    }
  ],
  "count": 1
}
```

### Error Response Example
```json
{
  "message": "Invalid date format. Use YYYY-MM-DD"
}
```
