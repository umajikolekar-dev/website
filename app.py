import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Example route for testing
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>🚀 Website is Live!</h1>
    <p>Your FastAPI backend is running successfully on Render.</p>
    """

# Notes endpoint (you can expand this later)
@app.get("/notes")
def get_notes():
    return {"notes": ["Chapter 1 - Basics", "Chapter 2 - Dynamics", "Chapter 3 - Vibrations"]}

# Attendance endpoint (demo)
@app.post("/attendance/{student_id}")
def mark_attendance(student_id: int):
    return {"status": "success", "student_id": student_id}

if __name__ == "__main__":
    # Render provides PORT dynamically
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
