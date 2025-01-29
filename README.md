# MexaHackathon2025Mentalytics

# Therapy Management System API Documentation

## Overview
This API provides endpoints for managing a therapy system focused on social anxiety assessment using the Liebowitz Social Anxiety Scale (LSAS). It supports both doctor and patient management, survey submissions, and progress tracking.

## Base URL
```
http://localhost:8000
```

## Authentication
*Note: Current implementation uses basic password hashing. In production, implement proper authentication and authorization.*

## Endpoints

### User Management

#### Register Doctor
```http
POST /doctors/register
```
Register a new doctor in the system.

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "name": "string",
    "specialization": "string"
}
```

#### Register Patient
```http
POST /patients/register
```
Register a new patient in the system.

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "name": "string",
    "doctor_id": integer
}
```

### LSAS Survey Management

#### Submit LSAS Survey
```http
POST /patients/{patient_id}/lsas-survey
```
Submit a new LSAS survey for a patient.

**Request Body:**
```json
{
    "responses": [
        {
            "question_id": integer,
            "fear_rating": integer (0-3),
            "avoidance_rating": integer (0-3)
        }
    ]
}
```

#### Get LSAS Progress
```http
GET /patients/{patient_id}/lsas-progress?timeframe={week|month|year}
```
Retrieve LSAS survey progress for a specific patient.

#### Get Latest LSAS
```http
GET /patients/{patient_id}/latest-lsas
```
Retrieve the most recent LSAS survey results for a patient.

### Doctor Dashboard

#### Get Patient Surveys
```http
GET /doctors/{doctor_id}/patient-surveys
```
Retrieve all patient surveys for a specific doctor.

#### Get All Doctors
```http
GET /doctors/?skip={skip}&limit={limit}
```
Retrieve a list of all doctors with pagination support.

### Analytics

#### Get Patient Analytics
```http
GET /patients/{patient_id}/analytics
```
Retrieve comprehensive analytics for a specific patient.

**Response:**
```json
{
    "total_surveys": integer,
    "average_score": float,
    "highest_score": integer,
    "lowest_score": integer,
    "current_anxiety_level": string,
    "score_history": [
        {
            "date": "datetime",
            "score": integer,
            "anxiety_level": string
        }
    ]
}
```

### LSAS Questions

#### Get LSAS Questions
```http
GET /api/lsas/questions
```
Retrieve the complete list of LSAS questions with rating scales.

## Data Models

### Anxiety Levels
The system uses the following anxiety levels based on total LSAS scores:
- No social anxiety (< 30)
- Mild social anxiety (30-49)
- Moderate social anxiety (50-64)
- Marked social anxiety (65-79)
- Severe social anxiety (80-94)
- Very severe social anxiety (≥ 95)

### Rating Scales
- Fear Scale:
  - 0: None
  - 1: Mild
  - 2: Moderate
  - 3: Severe

- Avoidance Scale:
  - 0: Never
  - 1: Occasionally
  - 2: Often
  - 3: Usually

## Error Handling
The API returns standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

Error responses include a detail message explaining the error.

## Database Schema
The system uses SQLite with the following main tables:
- doctors
- patients
- lsas_surveys
- recommendations
- assigned_exercises

## Development Setup
1. Install dependencies:
```bash
pip install fastapi sqlalchemy pydantic uvicorn
```

2. Run the server:
```bash
uvicorn app:app --reload
```

## Production Considerations
- Implement proper authentication and authorization
- Use secure password hashing
- Add rate limiting
- Set up proper CORS policies
- Use a production-grade database
- Implement proper logging and monitoring
- Add input validation and sanitization
- Set up proper error handling and reporting