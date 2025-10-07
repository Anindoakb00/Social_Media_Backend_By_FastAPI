# Social_Media_Backend_By_FastAPI

Minimal FastAPI backend intended for Render deployment.

What's in this repo
- app/ - FastAPI application
- alembic/ - database migrations
- requirements.txt - Python dependencies

Render quick deploy
1) Create a Web Service on Render and connect this GitHub repo.
2) Add these Environment variables in the Render service settings:
	- DATABASE_URL (postgresql://...)
	- SECRET_KEY
	- ALGORITHM (e.g. HS256)
	- ACCESS_TOKEN_EXPIRE_MINUTES (e.g. 30)
3) Set Build Command: pip install -r requirements.txt
4) Set Start Command: gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT

Notes
- Do NOT commit `.env` or other secrets. Use Render's Environment settings.
- This repository intentionally excludes Docker/CI/test artifacts for a minimal deploy.

If you'd like I can add an automated migration step (render.yaml or GitHub Actions) later.
2. Install dependencies:
