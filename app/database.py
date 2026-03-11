import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use TEST_DATABASE_URL for tests (SQLite in-memory), else use DATABASE_URL (PostgreSQL)
DATABASE_URL = os.getenv("TEST_DATABASE_URL") or os.getenv(
    "DATABASE_URL", "sqlite:///./hrms_local.db"
)

# SQLite needs special connect_args; PostgreSQL does not
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
