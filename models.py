from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Transcript(Document):
    audio_source: str
    content: Optional[str] = None
    status: str
    created_time: datetime = Field(default_factory=datetime.utcnow)
    updated_time: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "transcripts"