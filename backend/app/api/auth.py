from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.hash import bcrypt
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "super-secret"  

USERS = {}

class User(BaseModel):
    nickname: str
    password: str

def create_token(username: str):
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm="HS256")

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

@app.post("/register")
def register(user: User):
    if user.nickname in USERS:
        raise HTTPException(status_code=400, detail="Nickname taken")
    USERS[user.nickname] = bcrypt.hash(user.password)
    return {"msg": "Registered"}

@app.post("/login")
def login(user: User):
    hashed = USERS.get(user.nickname)
    if not hashed or not bcrypt.verify(user.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid login")
    token = create_token(user.nickname)
    return {"token": token, "nickname": user.nickname}

