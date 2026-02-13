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
        
        

# Company schemas
class CompanyCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    description: Optional[str] = None
    website: Optional[str] = None

class CompanyLogin(BaseModel):
    email: str
    password: str

class Company(BaseModel):
    id: int
    name: str
    email: str
    description: Optional[str]
    website: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Application schemas
class ApplicationCreate(BaseModel):
    job_id: int
    resume_id: int
    cover_letter: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    job_title: str
    company_name: str
    status: str
    applied_at: datetime
    
    class Config:
        from_attributes = True

class ApplicationDetailResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    user_email: str
    resume_id: int
    resume_filename: str
    job_id: int
    job_title: str
    status: str
    cover_letter: Optional[str]
    applied_at: datetime
    skills: List[str]
    similarity_score: Optional[float] = None
    
    class Config:
        from_attributes = True