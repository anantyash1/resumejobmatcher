#latest
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Float,
    Boolean,
    DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


# ======================
# USER
# ======================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="user")
    applications = relationship("Application", back_populates="user")


# ======================
# RESUME
# ======================
class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    raw_text = Column(Text, nullable=False)
    processed_text = Column(Text)
    skills = Column(Text)     # JSON string
    keywords = Column(Text)   # JSON string
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")


# ======================
# COMPANY (HR)
# ======================

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    description = Column(Text)
    website = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_hr = Column(Boolean, default=True)
    
    jobs = relationship("Job", back_populates="company_rel")
    applications = relationship("Application", back_populates="company")


# ======================
# JOB
# ======================
class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    salary_range = Column(String)
    job_type = Column(String)
    posted_date = Column(DateTime, default=datetime.utcnow)

    # ✅ FIXED RELATIONSHIPS
    company_rel = relationship("Company", back_populates="jobs")
    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")


# ======================
# JOB MATCH (AI Matching)
# ======================
class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    similarity_score = Column(Float)
    matched_skills = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Relationships
    job = relationship("Job", back_populates="matches")
    resume = relationship("Resume")



# ======================
# APPLICATION
# ======================
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    status = Column(String, default="pending")  # pending, reviewed, shortlisted, rejected
    cover_letter = Column(Text)
    applied_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime)

    user = relationship("User", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    company = relationship("Company", back_populates="applications")
