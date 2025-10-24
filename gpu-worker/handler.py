"""
RunPod Serverless Handler for Editto Video Editing
This handler receives video editing requests and processes them using the Editto model
"""

import runpod
import os
import sys
import requests
import subprocess
from pathlib import Path
import boto3
from botocore.exceptions import ClientError

# Add ditto to Python path
sys.path.append('/app/ditto')

# Environment variables for R2 storage
R2_ENDPOINT = os.environ.get('R2_ENDPOINT')
R2_ACCESS_KEY = os.environ.get('R2_ACCESS_KEY')
R2_SECRET_KEY = os.environ.get('R2_SECRET_KEY')
R2_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME', 'editto-videos')
R2_PUBLIC_URL = os.environ.get('R2_PUBLIC_URL')

# Initialize S3 client for R2
s3_client = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    region_name='auto'
)


def download_video(url: str, output_path: str) -> str:
    """Download video from URL"""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return output_path


def upload_to_r2(file_path: str, filename: str) -> str:
    """Upload file to Cloudflare R2"""
    try:
        with open(file_path, 'rb') as f:
            s3_client.put_object(
                Bucket=R2_BUCKET_NAME,
                Key=filename,
                Body=f,
                ContentType='video/mp4'
            )

        return f"{R2_PUBLIC_URL}/{filename}"
    except ClientError as e:
        raise Exception(f"Failed to upload to R2: {str(e)}")


def process_video(video_path: str, instruction: str, output_path: str) -> str:
    """
    Process video using Editto model

    NOTE: This is a placeholder implementation. You'll need to:
    1. Download the Editto model weights
    2. Implement the actual inference code based on the Editto repository
    3. Adjust parameters based on your GPU capacity

    For now, this demonstrates the structure and workflow
    """

    try:
        # TODO: Replace this with actual Editto inference code
        # This would involve:
        # 1. Loading the model
        # 2. Processing the video with the instruction
        # 3. Saving the edited video

        # Placeholder: Copy input to output (replace with actual processing)
        import shutil
        shutil.copy(video_path, output_path)

        print(f"Processing video with instruction: {instruction}")
        print("NOTE: This is a placeholder. Implement actual Editto inference here.")

        # Actual implementation would look something like:
        # from editto_inference import EdittoModel
        # model = EdittoModel.load('/app/models')
        # edited_video = model.edit(video_path, instruction)
        # edited_video.save(output_path)

        return output_path

    except Exception as e:
        raise Exception(f"Video processing failed: {str(e)}")


def handler(event):
    """
    RunPod handler function
    Expected input format:
    {
        "input": {
            "video_url": "https://...",
            "instruction": "make the sky sunset colors"
        }
    }
    """

    try:
        # Extract input parameters
        job_input = event.get("input", {})
        video_url = job_input.get("video_url")
        instruction = job_input.get("instruction")
        job_id = event.get("id", "unknown")

        if not video_url or not instruction:
            return {
                "error": "Missing required parameters: video_url and instruction"
            }

        print(f"Processing job {job_id}")
        print(f"Video URL: {video_url}")
        print(f"Instruction: {instruction}")

        # Create temporary paths
        input_path = f"/tmp/input_{job_id}.mp4"
        output_path = f"/tmp/output_{job_id}.mp4"

        # Download input video
        print("Downloading video...")
        download_video(video_url, input_path)

        # Process video with Editto
        print("Processing video with Editto...")
        process_video(input_path, instruction, output_path)

        # Upload result to R2
        print("Uploading result...")
        output_filename = f"edited/{job_id}.mp4"
        edited_video_url = upload_to_r2(output_path, output_filename)

        # Clean up temporary files
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

        print(f"Job {job_id} completed successfully")

        return {
            "status": "completed",
            "edited_video_url": edited_video_url,
            "job_id": job_id
        }

    except Exception as e:
        print(f"Error processing job: {str(e)}")
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    print("Starting RunPod serverless handler...")
    runpod.serverless.start({"handler": handler})
