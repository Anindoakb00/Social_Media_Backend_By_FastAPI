from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media Backend API", description="A minimal FastAPI backend for posts, users, auth and voting")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from app/static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    try:
        with open("app/static/index.html", "r", encoding="utf-8") as f:
            html = f.read()
    except Exception:
        html = "<html><body><h1>Social Media Backend</h1><p>Visit /docs for API docs.</p></body></html>"
    return HTMLResponse(content=html)


