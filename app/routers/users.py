from fastapi import APIRouter, HTTPException
from app.database import users
from app.schemas import UserCreate
import app.database as db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(user: UserCreate):
    user_id = db.user_id_counter
    db.users[user_id] = {"id": user_id, **user.dict()}
    db.user_id_counter += 1
    return db.users[user_id]

@router.get("/")
def get_users():
    return list(users.values())

@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]
