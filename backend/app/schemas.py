from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Resume schemas
class ResumeResponse(BaseModel):
    id: int
    filename: str
    skills: List[str]
    keywords: List[str]
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# Job schemas
class JobBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    description: str
    requirements: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: Optional[str] = "Full-time"

class JobResponse(JobBase):
    id: int
    posted_date: datetime
    
    class Config:
        from_attributes = True

class JobMatchResponse(JobResponse):
    similarity_score: float
    matched_skills: List[str]
    
    class Config:
        from_attributes = True