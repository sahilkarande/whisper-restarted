# api_fastapi.py

from fastapi import FastAPI, HTTPException
from flask import Flask
from pydantic import BaseModel
from typing import List
from models import User  # Assuming this comes from models.py which is shared between Flask & FastAPI

# Create FastAPI instance
api = FastAPI()

# Pydantic model for response
class UserOut(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    phone: str | None = None
    is_admin: bool

    class Config:
        orm_mode = True

@api.get("/api/users", response_model=List[UserOut])
def get_users():
    try:
        users = User.query.all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")

@api.get("/api/user/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = User.query.get(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")
