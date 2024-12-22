from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.database import Base
import pytest
from alembic import command


# local machine
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

@pytest.fixture()
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
      yield db
  finally:
      db.close()
   


@pytest.fixture
def client(session):
  def override_get_db():

    try:
        yield session
    finally:
        session.close()
  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)



@pytest.fixture
def test_user(client):
    user_data = {
        "name": "John Doe",
        "email": "johndoe@gmail.com",
        "password": "john@123",
    }
    res = client.post("/users/", json=user_data)
    assert  res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user