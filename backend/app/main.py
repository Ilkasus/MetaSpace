import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users
from app.db import Base, engine
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware as StarletteCORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.proxy_headers import ProxyHeadersMiddleware

from fastapi.middleware.trustedhost import TrustedHostMiddleware as FastAPITrustedHost

from starlette.applications import Starlette
from starlette.routing import Mount

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "https://meta-space-nu.vercel.app",
    "https://meta-space-mswzhfapn-ilkasus-projects.vercel.app",
    "https://meta-space-oo2t7fmki-ilkasus-projects.vercel.app"
]

fastapi_app = FastAPI(title="MetaSpace API")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@fastapi_app.get("/")
def root():
    return {"message": "MetaSpace backend is running"}

fastapi_app.include_router(auth.router, prefix="/auth", tags=["Auth"])
fastapi_app.include_router(users.router, prefix="/users", tags=["Users"])

from starlette.middleware import Middleware
from starlette.routing import Mount
from starlette.applications import Starlette

app = Starlette(
    routes=[
        Mount("/socket.io", app=socket_app),  
        Mount("/", app=fastapi_app),        
    ]
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
