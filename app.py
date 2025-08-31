from fastapi import FastAPI, Response
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import csv
import io

app = FastAPI()

# Database
conn = sqlite3.connect("attendance.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rollno TEXT,
    name TEXT,
    timestamp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# Add default admin (username: admin, password: 1234)
try:
    cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ("admin", "1234"))
    conn.commit()
except:
    pass

class Attendance(BaseModel):
    rollno: str
    name: str

class AdminLogin(BaseModel):
    username: str
    password: str

@app.post("/attendance")
def mark_attendance(entry: Attendance):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO attendance (rollno, name, timestamp) VALUES (?, ?, ?)",
                   (entry.rollno, entry.name, timestamp))
    conn.commit()
    return {"message": f"Attendance marked for {entry.name} ({entry.rollno})"}

@app.post("/admin-login")
def admin_login(login: AdminLogin):
    cursor.execute("SELECT * FROM admins WHERE username=? AND password=?",
                   (login.username, login.password))
    admin = cursor.fetchone()

    if admin:
        cursor.execute("SELECT rollno, name, timestamp FROM attendance")
        records = [{"rollno": r[0], "name": r[1], "timestamp": r[2]} for r in cursor.fetchall()]
        return {"success": True, "records": records}
    else:
        return {"success": False, "records": []}

@app.get("/download-attendance")
def download_attendance():
    # Create CSV in memory
    cursor.execute("SELECT rollno, name, timestamp FROM attendance")
    rows = cursor.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Roll No", "Name", "Timestamp"])
    writer.writerows(rows)

    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=attendance.csv"
    return response
