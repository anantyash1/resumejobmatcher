import json
from datetime import datetime
from ..database import SessionLocal
from ..models import Job

def seed_jobs():
    """Seed database with sample jobs"""
    db = SessionLocal()
    
    # Check if jobs already exist
    existing_jobs = db.query(Job).count()
    if existing_jobs > 0:
        print(f"Database already has {existing_jobs} jobs. Skipping seed.")
        return
    
    try:
        with open('data/sample_jobs.json', 'r') as f:
            jobs_data = json.load(f)
        
        for job_data in jobs_data:
            job = Job(**job_data)
            db.add(job)
        
        db.commit()
        print(f"Successfully seeded {len(jobs_data)} jobs!")
        
    except Exception as e:
        print(f"Error seeding jobs: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_jobs()