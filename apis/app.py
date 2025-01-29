from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from models.user import (
    LSASSurveyCreate,
    LSASSurveyResponse,
    LSASSurveyResult,
    DoctorCreate,
    DoctorResponse,
    PatientCreate,
    PatientResponse,
)
from models.lsas import (
    get_anxiety_level,
    FearLevel,
    AvoidanceLevel,
    Question,
    LSASQuestions,
)
from database.utils import get_db
from database.database_creation import LSASSurvey, Patient, Doctor

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# User Registration Routes
@app.post("/doctors/register", response_model=DoctorResponse)
def register_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    # Check if username exists
    db_doctor = db.query(Doctor).filter(Doctor.username == doctor.username).first()
    if db_doctor:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if email exists
    db_doctor = db.query(Doctor).filter(Doctor.email == doctor.email).first()
    if db_doctor:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new doctor
    db_doctor = Doctor(
        username=doctor.username,
        email=doctor.email,
        hashed_password=doctor.password,  # In production, use proper password hashing
        name=doctor.name,
        specialization=doctor.specialization,
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@app.post("/patients/{patient_id}/lsas-survey", response_model=LSASSurveyResult)
def submit_lsas_survey(
    patient_id: int, survey: LSASSurveyResponse, db: Session = Depends(get_db)
):
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Validate we have responses for all 24 questions
    if len(survey.responses) != 24:
        raise HTTPException(
            status_code=400, detail="Must provide responses for all 24 LSAS questions"
        )

    # Validate question IDs
    question_ids = sorted([r.question_id for r in survey.responses])
    expected_ids = list(range(1, 25))  # 1-24
    if question_ids != expected_ids:
        raise HTTPException(
            status_code=400, detail="Invalid or duplicate question IDs provided"
        )

    # Calculate total scores
    fear_total = sum(r.fear_rating for r in survey.responses)
    avoidance_total = sum(r.avoidance_rating for r in survey.responses)
    total_score = fear_total + avoidance_total

    # Calculate anxiety level
    anxiety_level = get_anxiety_level(total_score)

    # Create survey entry
    db_survey = LSASSurvey(
        patient_id=patient_id,
        total_score=total_score,
        anxiety_level=anxiety_level.value,
        submission_date=datetime.utcnow(),
    )

    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)

    return db_survey


@app.post("/patients/register", response_model=PatientResponse)
def register_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    # Check if username exists
    db_patient = db.query(Patient).filter(Patient.username == patient.username).first()
    if db_patient:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if email exists
    db_patient = db.query(Patient).filter(Patient.email == patient.email).first()
    if db_patient:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == patient.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Create new patient
    db_patient = Patient(
        username=patient.username,
        email=patient.email,
        hashed_password=patient.password,  # In production, use proper password hashing
        name=patient.name,
        doctor_id=patient.doctor_id,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


# Get all doctors
@app.get("/doctors/", response_model=List[DoctorResponse])
def get_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).offset(skip).limit(limit).all()
    return doctors


@app.get("/patients/{patient_id}/lsas-progress")
def get_lsas_progress(
    patient_id: int,
    timeframe: str,  # 'week', 'month', 'year'
    db: Session = Depends(get_db),
):
    surveys = (
        db.query(LSASSurvey)
        .filter(LSASSurvey.patient_id == patient_id)
        .order_by(LSASSurvey.submission_date.desc())
        .all()
    )

    return {
        "surveys": [
            {
                "date": survey.submission_date,
                "score": survey.total_score,
                "anxiety_level": survey.anxiety_level,
            }
            for survey in surveys
        ]
    }


@app.get("/patients/{patient_id}/latest-lsas")
def get_latest_lsas(patient_id: int, db: Session = Depends(get_db)):
    latest_survey = (
        db.query(LSASSurvey)
        .filter(LSASSurvey.patient_id == patient_id)
        .order_by(LSASSurvey.submission_date.desc())
        .first()
    )

    if not latest_survey:
        raise HTTPException(status_code=404, detail="No surveys found")

    return {
        "score": latest_survey.total_score,
        "anxiety_level": latest_survey.anxiety_level,
        "date": latest_survey.submission_date,
    }


# Doctor Dashboard Routes
@app.get("/doctors/{doctor_id}/patient-surveys")
def get_doctor_patient_surveys(doctor_id: int, db: Session = Depends(get_db)):
    # Get all patients for the doctor with their latest surveys
    patients = db.query(Patient).filter(Patient.doctor_id == doctor_id).all()

    patient_surveys = []
    for patient in patients:
        latest_survey = (
            db.query(LSASSurvey)
            .filter(LSASSurvey.patient_id == patient.id)
            .order_by(LSASSurvey.submission_date.desc())
            .first()
        )

        patient_surveys.append(
            {
                "patient_id": patient.id,
                "patient_name": patient.name,
                "latest_survey": (
                    {
                        "score": latest_survey.total_score,
                        "anxiety_level": latest_survey.anxiety_level,
                        "date": latest_survey.submission_date,
                    }
                    if latest_survey
                    else None
                ),
            }
        )

    # Sort by latest survey date
    return sorted(
        patient_surveys,
        key=lambda x: (
            x["latest_survey"]["date"] if x["latest_survey"] else datetime.min
        ),
        reverse=True,
    )


@app.get("/patients/{patient_id}/analytics")
def get_patient_analytics(patient_id: int, db: Session = Depends(get_db)):
    surveys = (
        db.query(LSASSurvey)
        .filter(LSASSurvey.patient_id == patient_id)
        .order_by(LSASSurvey.submission_date)
        .all()
    )

    if not surveys:
        raise HTTPException(status_code=404, detail="No surveys found")

    # Calculate analytics
    scores = [survey.total_score for survey in surveys]
    return {
        "total_surveys": len(surveys),
        "average_score": sum(scores) / len(scores),
        "highest_score": max(scores),
        "lowest_score": min(scores),
        "current_anxiety_level": surveys[-1].anxiety_level,
        "score_history": [
            {
                "date": survey.submission_date,
                "score": survey.total_score,
                "anxiety_level": survey.anxiety_level,
            }
            for survey in surveys
        ],
    }


@app.get("/api/lsas/questions", response_model=LSASQuestions)
async def get_lsas_questions():
    questions_data = [
        {"id": 1, "situation": "Using a telephone in public"},
        {"id": 2, "situation": "Participating in a small group activity"},
        {"id": 3, "situation": "Eating in public"},
        {"id": 4, "situation": "Drinking with others"},
        {"id": 5, "situation": "Talking to someone in authority"},
        {
            "id": 6,
            "situation": "Acting, performing, or speaking in front of an audience",
        },
        {"id": 7, "situation": "Going to a party"},
        {"id": 8, "situation": "Working while being observed"},
        {"id": 9, "situation": "Writing while being observed"},
        {"id": 10, "situation": "Calling someone you don't know very well"},
        {
            "id": 11,
            "situation": "Talking face to face with someone you don't know very well",
        },
        {"id": 12, "situation": "Meeting strangers"},
        {"id": 13, "situation": "Urinating in a public bathroom"},
        {"id": 14, "situation": "Entering a room when others are already seated"},
        {"id": 15, "situation": "Being the center of attention"},
        {"id": 16, "situation": "Speaking up at a meeting"},
        {"id": 17, "situation": "Taking a test of your ability, skill, or knowledge"},
        {
            "id": 18,
            "situation": "Expressing disagreement or disapproval to someone you don't know very well",
        },
        {
            "id": 19,
            "situation": "Looking someone who you don't know very well straight in the eyes",
        },
        {"id": 20, "situation": "Giving a prepared oral talk to a group"},
        {
            "id": 21,
            "situation": "Trying to make someone's acquaintance for the purpose of a romantic/sexual relationship",
        },
        {"id": 22, "situation": "Returning goods to a store for a refund"},
        {"id": 23, "situation": "Giving a party"},
        {"id": 24, "situation": "Resisting a high pressure sales person"},
    ]

    fear_options = [level.value for level in FearLevel]
    avoidance_options = [level.value for level in AvoidanceLevel]

    questions = [
        Question(
            id=q["id"],
            situation=q["situation"],
            fear_options=fear_options,
            avoidance_options=avoidance_options,
        )
        for q in questions_data
    ]

    return LSASQuestions(
        questions=questions,
        fear_scale={"0": "None", "1": "Mild", "2": "Moderate", "3": "Severe"},
        avoidance_scale={
            "0": "Never",
            "1": "Occasionally",
            "2": "Often",
            "3": "Usually",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
