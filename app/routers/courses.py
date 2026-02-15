from fastapi import APIRouter, HTTPException, Query
from app.database import courses
from app.schemas import CourseCreate
import app.database as db

router = APIRouter(prefix="/courses", tags=["Courses"])

# Public: Get all courses
@router.get("/")
def get_courses():
    return list(courses.values())

# Public: Get course by ID
@router.get("/{course_id}")
def get_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

# Admin-only: Create course
@router.post("/")
def create_course(course: CourseCreate, role: str = Query(...)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    # Check unique code
    for c in courses.values():
        if c["code"] == course.code:
            raise HTTPException(status_code=400, detail="Course code must be unique")

    course_id = db.course_id_counter
    db.courses[course_id] = {"id": course_id, **course.dict()}
    db.course_id_counter += 1
    return db.courses[course_id]

# Admin-only: Update course
@router.put("/{course_id}")
def update_course(course_id: int, course: CourseCreate, role: str = Query(...)):
    if role != "admin":
        raise HTTPException(status_code=403)

    if course_id not in courses:
        raise HTTPException(status_code=404)

    # Update course details
    courses[course_id].update(course.dict())
    return courses[course_id]

# Admin-only: Delete course
@router.delete("/{course_id}")
def delete_course(course_id: int, role: str = Query(...)):
    if role != "admin":
        raise HTTPException(status_code=403)

    if course_id not in courses:
        raise HTTPException(status_code=404)

    del courses[course_id]
    return {"message": "Deleted"}
