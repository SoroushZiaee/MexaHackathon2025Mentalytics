from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Float,
    Enum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

from datetime import datetime

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./therapy_system.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Base = declarative_base()


# SQLAlchemy Models
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    specialization = Column(String)
    patients = relationship("Patient", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    doctor = relationship("Doctor", back_populates="patients")
    surveys = relationship("LSASSurvey", back_populates="patient")
    exercises = relationship("AssignedExercise", back_populates="patient")


class LSASSurvey(Base):
    __tablename__ = "lsas_surveys"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    submission_date = Column(DateTime, default=datetime.utcnow)
    total_score = Column(Integer)
    anxiety_level = Column(String)
    patient = relationship("Patient", back_populates="surveys")
    recommendations = relationship("Recommendation", back_populates="survey")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("lsas_surveys.id"))
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    survey = relationship("LSASSurvey", back_populates="recommendations")
    selected = Column(Boolean, default=False)


class AssignedExercise(Base):
    __tablename__ = "assigned_exercises"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    assigned_date = Column(DateTime, default=datetime.utcnow)
    content = Column(String)
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    patient = relationship("Patient", back_populates="exercises")


# Create tables
Base.metadata.create_all(bind=engine)
