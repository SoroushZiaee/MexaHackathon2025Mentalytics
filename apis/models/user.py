from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List, Annotated
from datetime import datetime


# Pydantic Models
class UserLogin(BaseModel):
    username: str
    password: str


class DoctorCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str
    specialization: str


class DoctorResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    name: str
    specialization: str

    class Config:
        orm_mode = True


class PatientCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str
    doctor_id: int


class PatientResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    name: str
    doctor_id: int

    class Config:
        orm_mode = True


# Pydantic models for request validation
class QuestionResponse(BaseModel):
    question_id: int
    fear_rating: int  # Validates rating is between 0-3
    avoidance_rating: int  # Validates rating is between 0-3


class LSASSurveyCreate(BaseModel):
    responses: List[QuestionResponse]


class QuestionResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"question_id": 1, "fear_rating": 2, "avoidance_rating": 1}
        }
    )

    question_id: int
    fear_rating: Annotated[int, Field(ge=0, le=3)]
    avoidance_rating: Annotated[int, Field(ge=0, le=3)]


class LSASSurveyResponse(BaseModel):
    responses: List[QuestionResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "responses": [
                    {"question_id": 1, "fear_rating": 0, "avoidance_rating": 0},
                    {"question_id": 2, "fear_rating": 1, "avoidance_rating": 1},
                    {"question_id": 3, "fear_rating": 2, "avoidance_rating": 1},
                    {"question_id": 4, "fear_rating": 1, "avoidance_rating": 2},
                    {"question_id": 5, "fear_rating": 2, "avoidance_rating": 2},
                    {"question_id": 6, "fear_rating": 3, "avoidance_rating": 3},
                    {"question_id": 7, "fear_rating": 2, "avoidance_rating": 2},
                    {"question_id": 8, "fear_rating": 1, "avoidance_rating": 1},
                    {"question_id": 9, "fear_rating": 1, "avoidance_rating": 0},
                    {"question_id": 10, "fear_rating": 2, "avoidance_rating": 2},
                    {"question_id": 11, "fear_rating": 2, "avoidance_rating": 1},
                    {"question_id": 12, "fear_rating": 3, "avoidance_rating": 2},
                    {"question_id": 13, "fear_rating": 1, "avoidance_rating": 0},
                    {"question_id": 14, "fear_rating": 2, "avoidance_rating": 1},
                    {"question_id": 15, "fear_rating": 3, "avoidance_rating": 3},
                    {"question_id": 16, "fear_rating": 2, "avoidance_rating": 2},
                    {"question_id": 17, "fear_rating": 2, "avoidance_rating": 1},
                    {"question_id": 18, "fear_rating": 2, "avoidance_rating": 2},
                    {"question_id": 19, "fear_rating": 1, "avoidance_rating": 1},
                    {"question_id": 20, "fear_rating": 3, "avoidance_rating": 2},
                    {"question_id": 21, "fear_rating": 3, "avoidance_rating": 3},
                    {"question_id": 22, "fear_rating": 1, "avoidance_rating": 1},
                    {"question_id": 23, "fear_rating": 2, "avoidance_rating": 2},
                    {"question_id": 24, "fear_rating": 1, "avoidance_rating": 1},
                ]
            }
        }
    )

    responses: List[QuestionResponse]


class LSASSurveyResult(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "submission_date": "2024-01-29T10:00:00",
                "total_score": 79,
                "anxiety_level": "Marked social anxiety",
            }
        }
    )

    id: int
    submission_date: datetime
    total_score: int
    anxiety_level: str


class ExerciseAssign(BaseModel):
    content: str
    patient_id: int
