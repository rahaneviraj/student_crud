from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database setup
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT,
    contact TEXT
)
""")
conn.commit()

class Student(BaseModel):
    name: str
    dob: str
    contact: str

@app.post("/students")
def create_student(student: Student):
    cursor.execute("INSERT INTO students (name, dob, contact) VALUES (?, ?, ?)",
                   (student.name, student.dob, student.contact))
    conn.commit()
    return {"message": "Student added successfully"}

@app.get("/students")
def get_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()

@app.get("/students/{student_id}")
def get_student(student_id: int):
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = cursor.fetchone()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    cursor.execute("UPDATE students SET name=?, dob=?, contact=? WHERE id=?",
                   (student.name, student.dob, student.contact, student_id))
    conn.commit()
    return {"message": "Student updated successfully"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    return {"message": "Student deleted successfully"}
