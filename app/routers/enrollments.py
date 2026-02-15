from fastapi import APIRouter, HTTPException
from app.database import users, courses, enrollments
from app.schemas import EnrollmentCreate
import app.database as db

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

# Student enroll in course
@router.post("/")
def enroll(data: EnrollmentCreate):
    if data.role != "student":
        raise HTTPException(status_code=403, detail="Students only")

    if data.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    if data.course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    # Prevent double enrollment
    for e in enrollments.values():
        if e["user_id"] == data.user_id and e["course_id"] == data.course_id:
            raise HTTPException(status_code=400, detail="Already enrolled")

    enrollment_id = db.enrollment_id_counter
    db.enrollments[enrollment_id] = {
        "id": enrollment_id,
        "user_id": data.user_id,
        "course_id": data.course_id
    }
    db.enrollment_id_counter += 1
    return db.enrollments[enrollment_id]

# Get all enrollments for a student
@router.get("/student/{user_id}")
def get_student_enrollments(user_id: int):
    return [e for e in enrollments.values() if e["user_id"] == user_id]

# Admin: Get all enrollments
@router.get("/")
def get_all_enrollments(role: str):
    if role != "admin":
        raise HTTPException(status_code=403)
    return list(enrollments.values())

# Deregister student (student or admin)
@router.delete("/{enrollment_id}")
def deregister(enrollment_id: int, role: str):
    if role not in ["student", "admin"]:
        raise HTTPException(status_code=403)
    if enrollment_id not in enrollments:
        raise HTTPException(status_code=404)
    del enrollments[enrollment_id]
    return {"message": "Deregistered"}
