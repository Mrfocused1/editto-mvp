from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    instruction = Column(Text, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    original_video_url = Column(String, nullable=True)
    edited_video_url = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
