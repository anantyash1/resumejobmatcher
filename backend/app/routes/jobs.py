import json
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Resume, Job, JobMatch
from ..schemas import JobMatchResponse
from ..auth import get_current_user
from ..services.job_matcher import JobMatcher

router = APIRouter(prefix="/jobs", tags=["jobs"])

job_matcher = JobMatcher()

@router.get("/recommendations", response_model=list[JobMatchResponse])
def get_job_recommendations(
    resume_id: int = Query(..., description="Resume ID to match against"),
    top_n: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get job recommendations for a resume"""
    
    # Verify resume belongs to user
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Get all jobs
    jobs = db.query(Job).all()
    
    if not jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No jobs available in database"
        )
    
    # Convert to dict format
    jobs_data = [
        {
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'description': job.description,
            'requirements': job.requirements or '',
            'salary_range': job.salary_range,
            'job_type': job.job_type,
            'posted_date': job.posted_date
        }
        for job in jobs
    ]
    
    # Get resume data
    resume_skills = json.loads(resume.skills) if resume.skills else []
    
    # Match jobs
    matches = job_matcher.match_jobs(
        resume_text=resume.processed_text or resume.raw_text,
        resume_skills=resume_skills,
        jobs=jobs_data,
        top_n=top_n
    )
    
    # Save matches to database
    for match in matches:
        job_match = JobMatch(
            resume_id=resume.id,
            job_id=match['job']['id'],
            similarity_score=match['similarity_score'],
            matched_skills=json.dumps(match['matched_skills'])
        )
        db.merge(job_match)
    
    db.commit()
    
    # Format response
    results = []
    for match in matches:
        job = match['job']
        results.append({
            'id': job['id'],
            'title': job['title'],
            'company': job['company'],
            'location': job['location'],
            'description': job['description'],
            'requirements': job['requirements'],
            'salary_range': job['salary_range'],
            'job_type': job['job_type'],
            'posted_date': job['posted_date'],
            'similarity_score': match['similarity_score'],
            'matched_skills': match['matched_skills']
        })
    
    return results