from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, Application, Job, Resume, Company
from ..schemas import ApplicationCreate, ApplicationResponse
from ..auth import get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/apply", response_model=ApplicationResponse)
def apply_to_job(
    application: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Apply to a job"""
    
    # Check if job exists
    job = db.query(Job).filter(Job.id == application.job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check if resume belongs to user
    resume = db.query(Resume).filter(
        Resume.id == application.resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Check if already applied
    existing_application = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.job_id == application.job_id
    ).first()
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied to this job"
        )
    
    # Get company_id from job
    company = db.query(Company).filter(Company.name == job.company).first()
    company_id = company.id if company else 1  # Default to 1 if not found
    
    # Create application
    new_application = Application(
        user_id=current_user.id,
        resume_id=application.resume_id,
        job_id=application.job_id,
        company_id=company_id,
        cover_letter=application.cover_letter,
        status="pending"
    )
    
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    
    return {
        "id": new_application.id,
        "job_id": job.id,
        "job_title": job.title,
        "company_name": job.company,
        "status": new_application.status,
        "applied_at": new_application.applied_at
    }

@router.get("/my-applications", response_model=List[ApplicationResponse])
def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all applications for current user"""
    
    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).order_by(Application.applied_at.desc()).all()
    
    results = []
    for app in applications:
        job = db.query(Job).filter(Job.id == app.job_id).first()
        results.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": job.title if job else "Unknown",
            "company_name": job.company if job else "Unknown",
            "status": app.status,
            "applied_at": app.applied_at
        })
    
    return results

@router.get("/check/{job_id}")
def check_application_status(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user has applied to a job"""
    
    application = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.job_id == job_id
    ).first()
    
    return {
        "has_applied": application is not None,
        "status": application.status if application else None,
        "applied_at": application.applied_at if application else None
    }