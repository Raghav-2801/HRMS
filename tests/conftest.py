import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use SQLite in-memory for all tests
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test_hrms.db"

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

TEST_DB_URL = "sqlite:///./test_hrms.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_employee(client):
    payload = {
        "employee_id": "EMP001",
        "name": "Kapil Raghav",
        "email": "kapil@example.com",
        "department": "Engineering",
        "position": "Backend Developer",
    }
    resp = client.post("/api/employees/", json=payload)
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def sample_employee_2(client):
    payload = {
        "employee_id": "EMP002",
        "name": "Rahul Singh",
        "email": "rahul@example.com",
        "department": "HR",
    }
    resp = client.post("/api/employees/", json=payload)
    assert resp.status_code == 201
    return resp.json()
