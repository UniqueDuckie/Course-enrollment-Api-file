from fastapi import FastAPI
from app.routers import users, courses, enrollments

app = FastAPI()

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
