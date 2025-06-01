import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users
from app.db import Base, engine
import uvicorn

app = FastAPI(title="MetaSpace API")

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "https://meta-space-nu.vercel.app",
    "https://meta-space-mswzhfapn-ilkasus-projects.vercel.app",
    "https://meta-space-oo2t7fmki-ilkasus-projects.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "MetaSpace backend is running"}

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
