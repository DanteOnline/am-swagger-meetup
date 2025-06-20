from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import uvicorn
from models import Base, VideoDetectionEvent
from schemas import (
    VideoDetectionEventCreate,
    VideoDetectionEventOut,
    VideoDetectionEventUpdate
)


DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/events/", response_model=VideoDetectionEventOut, status_code=201)
def create_event(event: VideoDetectionEventCreate, db: Session = Depends(get_db)):
    db_event = VideoDetectionEvent(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/events/", response_model=List[VideoDetectionEventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(VideoDetectionEvent).all()

@app.get("/events/{event_id}/", response_model=VideoDetectionEventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(VideoDetectionEvent).filter(VideoDetectionEvent.id == event_id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    return event

@app.put("/events/{event_id}/", response_model=VideoDetectionEventOut)
def put_event(event_id: int, update: VideoDetectionEventCreate, db: Session = Depends(get_db)):
    event = db.query(VideoDetectionEvent).filter(VideoDetectionEvent.id == event_id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    for field, value in update.model_dump().items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event

@app.patch("/events/{event_id}/", response_model=VideoDetectionEventOut)
def patch_event(event_id: int, update: VideoDetectionEventUpdate, db: Session = Depends(get_db)):
    event = db.query(VideoDetectionEvent).filter(VideoDetectionEvent.id == event_id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event

@app.delete("/events/{event_id}/", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(VideoDetectionEvent).filter(VideoDetectionEvent.id == event_id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    db.delete(event)
    db.commit()


if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("main:app", reload=True)
