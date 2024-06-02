from pydantic import BaseModel
from typing import Optional


class TranscriptCreate(BaseModel):
    audio_source: str
    content: Optional[str] = None
    status: str