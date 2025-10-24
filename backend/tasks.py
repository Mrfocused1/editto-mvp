from celery import Celery
import os
import requests
import time
from database import SessionLocal
import models

# Celery configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY", "")
RUNPOD_ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID", "")

celery_app = Celery(
    "editto_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@celery_app.task(name="tasks.process_video_task")
def process_video_task(job_id: str, video_url: str, instruction: str):
    """
    Process video using RunPod serverless endpoint
    """
    db = SessionLocal()
    try:
        # Update job status to processing
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if not job:
            return {"error": "Job not found"}

        job.status = "processing"
        db.commit()

        # Call RunPod endpoint
        # Note: This is a placeholder - you'll need to implement the actual RunPod API call
        # based on your specific endpoint setup

        headers = {
            "Authorization": f"Bearer {RUNPOD_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "input": {
                "video_url": video_url,
                "instruction": instruction
            }
        }

        # Submit job to RunPod
        response = requests.post(
            f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/run",
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"RunPod API error: {response.text}")

        result = response.json()
        runpod_job_id = result.get("id")

        # Poll for completion
        max_attempts = 60  # 10 minutes max (10 second intervals)
        for attempt in range(max_attempts):
            time.sleep(10)

            status_response = requests.get(
                f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/status/{runpod_job_id}",
                headers=headers,
                timeout=30
            )

            if status_response.status_code != 200:
                continue

            status_data = status_response.json()
            status = status_data.get("status")

            if status == "COMPLETED":
                edited_video_url = status_data.get("output", {}).get("edited_video_url")

                if edited_video_url:
                    job.status = "completed"
                    job.edited_video_url = edited_video_url
                    db.commit()
                    return {"status": "completed", "edited_video_url": edited_video_url}
                else:
                    raise Exception("No edited video URL in response")

            elif status == "FAILED":
                raise Exception(status_data.get("error", "Unknown error"))

        # Timeout
        raise Exception("Processing timeout - job took too long")

    except Exception as e:
        # Update job status to failed
        job.status = "failed"
        job.error_message = str(e)
        db.commit()
        return {"error": str(e)}

    finally:
        db.close()
