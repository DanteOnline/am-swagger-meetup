import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class VideoDetectionEvent(Base):
    __tablename__ = "video_detection_events"
    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(String, index=True)
    event_type = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    location = Column(String)
