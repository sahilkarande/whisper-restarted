# api_fastapi.py

from fastapi import FastAPI
from app.models import db, User
from flask import Flask
from pydantic import BaseModel

api = FastAPI()

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        orm_mode = True

@api.get("/api/users", response_model=list[UserOut])
def get_users():
    return User.query.all()

@api.get("/api/user/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = User.query.get(user_id)
    if user:
        return user
    return {"error": "User not found"}
