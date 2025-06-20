from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class VideoDetectionEventBase(BaseModel):
    camera_id: str
    event_type: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime
    location: str

class VideoDetectionEventCreate(VideoDetectionEventBase):
    pass

class VideoDetectionEventUpdate(BaseModel):
    camera_id: Optional[str] = None
    event_type: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    timestamp: Optional[datetime] = None
    location: Optional[str] = None

    model_config = {
        "form_attributes": True
    }


class VideoDetectionEventOut(VideoDetectionEventBase):
    id: int

    model_config = {
        "form_attributes": True
    }
