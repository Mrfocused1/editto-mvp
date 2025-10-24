from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import os
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from pydantic import BaseModel
from enum import Enum

# Import database models and session
from database import SessionLocal, engine, Base
import models
from tasks import process_video_task

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Editto API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
R2_ENDPOINT = os.getenv("R2_ENDPOINT", "")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY", "")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY", "")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "editto-videos")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "")

# Initialize S3 client for Cloudflare R2
s3_client = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    region_name='auto',
    config=Config(
        signature_version='s3v4',
        s3={'addressing_style': 'path'}
    )
)


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobResponse(BaseModel):
    id: str
    instruction: str
    status: str
    created_at: datetime
    original_video_url: str | None = None
    edited_video_url: str | None = None
    error_message: str | None = None


def upload_to_r2(file_content: bytes, filename: str) -> str:
    """Upload file to Cloudflare R2 and return public URL"""
    try:
        s3_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=filename,
            Body=file_content,
            ContentType='video/mp4'
        )

        # Return public URL
        return f"{R2_PUBLIC_URL}/{filename}"
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to R2: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Editto API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/debug/config")
async def debug_config():
    """Debug endpoint to verify environment variables (shows partial values only)"""
    return {
        "R2_ENDPOINT": R2_ENDPOINT,
        "R2_ACCESS_KEY": f"{R2_ACCESS_KEY[:10]}...{R2_ACCESS_KEY[-5:]}" if R2_ACCESS_KEY else "NOT SET",
        "R2_SECRET_KEY": f"{R2_SECRET_KEY[:10]}...{R2_SECRET_KEY[-5:]}" if R2_SECRET_KEY else "NOT SET",
        "R2_BUCKET_NAME": R2_BUCKET_NAME,
        "R2_PUBLIC_URL": R2_PUBLIC_URL,
    }


@app.post("/api/upload")
async def upload_video(
    video: UploadFile = File(...),
    instruction: str = Form(...)
):
    """Upload a video and create an editing job"""

    if not instruction.strip():
        raise HTTPException(status_code=400, detail="Instruction cannot be empty")

    # Validate file type
    if not video.content_type or not video.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")

    # Generate unique job ID and filename
    job_id = str(uuid.uuid4())
    file_extension = os.path.splitext(video.filename or "video.mp4")[1]
    original_filename = f"original/{job_id}{file_extension}"

    # Read file content
    file_content = await video.read()

    # Upload to R2
    original_video_url = upload_to_r2(file_content, original_filename)

    # Create database entry
    db = SessionLocal()
    try:
        db_job = models.Job(
            id=job_id,
            instruction=instruction,
            status=JobStatus.PENDING,
            original_video_url=original_video_url
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)

        # Queue the processing task
        process_video_task.delay(job_id, original_video_url, instruction)

        return {
            "job_id": job_id,
            "status": "pending",
            "message": "Video uploaded successfully and queued for processing"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")
    finally:
        db.close()


@app.get("/api/jobs", response_model=List[JobResponse])
async def get_jobs():
    """Get all jobs"""
    db = SessionLocal()
    try:
        jobs = db.query(models.Job).order_by(models.Job.created_at.desc()).all()
        return jobs
    finally:
        db.close()


@app.get("/api/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """Get a specific job by ID"""
    db = SessionLocal()
    try:
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
