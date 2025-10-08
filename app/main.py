from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
from .config import settings
import os


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


@app.get('/health')
def health(db: Session = Depends(get_db)):
    """Health check endpoint that verifies DB connectivity."""
    try:
        # lightweight test query
        db.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        # return a 503 so orchestrators can detect failure
        raise HTTPException(status_code=503, detail=str(e))


# Optional: create DB tables automatically when running in an environment where
# you cannot run alembic (e.g. some free hosting plans). Enable by setting
# AUTO_CREATE_TABLES=true in the environment. This should only be used as a
# temporary measure for testing / debugging.
if os.getenv('AUTO_CREATE_TABLES', '').lower() in ('1', 'true', 'yes'):
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception:
        # swallow on startup; health endpoint will reveal DB errors
        pass


