from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import os
import uvicorn
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# -----------------------------
# Database setup (SQLite)
# -----------------------------
DATABASE_URL = "sqlite:///./attendance.db"  # local SQLite file
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)

# -----------------------------
# API Endpoints
# -----------------------------

@app.get("/notes")
def get_notes():
    return {"notes": ["Chapter 1 - Basics", "Chapter 2 - Dynamics", "Chapter 3 - Vibrations"]}


@app.post("/attendance/{student_id}")
def mark_attendance(student_id: int):
    db = SessionLocal()
    record = Attendance(student_id=student_id, timestamp=datetime.utcnow())
    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()
    return {"status": "success", "student_id": student_id, "time": record.timestamp}


@app.get("/attendance")
def get_attendance():
    db = SessionLocal()
    records = db.query(Attendance).all()
    db.close()
    return [
        {"id": r.id, "student_id": r.student_id, "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
        for r in records
    ]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)

