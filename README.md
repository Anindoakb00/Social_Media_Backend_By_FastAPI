# Social_Media_Backend_By_FastAPI

This is a FastAPI-based backend for a simple social media application. The repository includes:

- FastAPI application with routers for posts, users, authentication, and votes
- SQLAlchemy models and Alembic migration scripts
- Utility functions for password hashing and OAuth2/JWT authentication
- Pytest-based tests for core functionality

This README contains quick setup and deployment instructions.

Requirements
------------
- Python 3.12+

Quick start (local)
-------------------
1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows: .venv\\Scripts\\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the required environment variables (see "Environment variables" below).

4. Run the app (development):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for the interactive API docs.

Environment variables
---------------------
Create a `.env` file in the repo root with these variables:

```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=yourpassword
SECRET_KEY=replace-with-a-secure-random-value
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Deployment
----------
This project includes a `Dockerfile` for containerized deployment. You can deploy to providers like Fly.io, Railway, Render or Cloud Run. See the repository for example CI workflow.

Contributing
------------
PRs welcome. Please open an issue first for larger changes.

License
-------
This project is provided as-is. Add your license file if you wish to open-source it.
