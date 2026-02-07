import os
import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Resume
from ..schemas import ResumeResponse
from ..auth import get_current_user
from ..services.resume_parser import ResumeParser
from ..services.nlp_processor import NLPProcessor

router = APIRouter(prefix="/resume", tags=["resume"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

resume_parser = ResumeParser()
nlp_processor = NLPProcessor()

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process resume"""
    
    # Validate file type
    allowed_extensions = ['.pdf', '.doc', '.docx', '.png', '.jpg', '.jpeg']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save file
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text
        raw_text = resume_parser.extract_text(file_path, file.filename)
        
        if not raw_text or len(raw_text) < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract sufficient text from resume"
            )
        
        # Process text
        processed_text = nlp_processor.preprocess_text(raw_text)
        skills = nlp_processor.extract_skills(raw_text)
        keywords = nlp_processor.extract_keywords(raw_text)
        
        # Save to database
        resume = Resume(
            user_id=current_user.id,
            filename=file.filename,
            raw_text=raw_text,
            processed_text=processed_text,
            skills=json.dumps(skills),
            keywords=json.dumps(keywords)
        )
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return {
            "id": resume.id,
            "filename": resume.filename,
            "skills": skills,
            "keywords": keywords,
            "uploaded_at": resume.uploaded_at
        }
        
    except Exception as e:
        # Clean up file if error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        )

@router.get("/my-resumes", response_model=list[ResumeResponse])
def get_my_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all resumes for current user"""
    
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "skills": json.loads(r.skills) if r.skills else [],
            "keywords": json.loads(r.keywords) if r.keywords else [],
            "uploaded_at": r.uploaded_at
        }
        for r in resumes
    ]