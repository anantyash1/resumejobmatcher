from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, resume, jobs
from .database import init_db

app = FastAPI(
    title="Resume Job Matcher API",
    description="Classical ML-based resume to job matching system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(jobs.router)

@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()

@app.get("/")
def root():
    return {
        "message": "Resume Job Matcher API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}