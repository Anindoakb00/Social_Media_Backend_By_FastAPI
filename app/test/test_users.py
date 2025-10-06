from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base.metadata.create_all(bind=engine)
Base = declarative_base()
def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
@pytest.fuxture
def client():
  return TestClient(app)

def test_root():
  def root():
    client.get("/")
    res = client.get("/")
    print(res.json().get('message'))
  
def test_creat_user():
  res = client.post(
    "/users/",json={"email": "hello123@gmail.com", "password": "password123"})
  new_user = schemas.UserOut(**res.json())
  assert new_user.email == "hello123@gmail.com"
  assert res.status_code == 201
