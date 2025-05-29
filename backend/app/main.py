import os
from fastapi import FastAPI
from app.api import users, auth
from socket_server import app

app = FastAPI()

@app.get("/")
def root():
    return {"message": "MetaSpace backend is running"}

@app.on_event("startup")
def on_startup():
    port = os.getenv("PORT", "8000")
    print(f"Starting app on port {port}")

# Routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
