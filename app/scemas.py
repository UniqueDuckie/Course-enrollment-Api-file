from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    role: Literal["student", "admin"]

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int
    role: Literal["student", "admin"]
