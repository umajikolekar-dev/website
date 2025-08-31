from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime

# 1. Create FastAPI app
app = FastAPI()

# 2. Enable CORS (so frontend on GitHub Pages / Render can connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Database setup
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 4. Routes

@app.get("/")
def home():
    return {"message": "Backend is running successfully!"}

@app.get("/notes")
def get_notes():
    # Later you can fetch from DB or folder
    return {"notes": ["Chapter 1.pdf", "Chapter 2.pdf", "Chapter 3.pdf"]}

@app.post("/attendance/{student_id}")
def mark_attendance(student_id: str):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (student_id, timestamp) VALUES (?, ?)",
                   (student_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return {"message": "Attendance marked", "student_id": student_id}

@app.get("/attendance")
def get_attendance():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, timestamp FROM attendance ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return [{"student_id": r[0], "timestamp": r[1]} for r in records]
