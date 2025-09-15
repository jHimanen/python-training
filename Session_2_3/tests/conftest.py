import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load .env.test file before reading environment variables
from dotenv import load_dotenv
from pathlib import Path

# Load .env.test file
ROOT = Path(__file__).resolve().parents[1]
env_test_path = ROOT / ".env.test"
if env_test_path.exists():
    load_dotenv(env_test_path)

# Make sure tests import your src/ code
import sys
SRC = ROOT / "src"
if SRC.exists():
    sys.path.insert(0, str(SRC))

# Import app bits AFTER sys.path tweak
from app.core.db import Base           # your Declarative Base (no engine here)
from app.main import app as fastapi_app               # FastAPI app
import app.models.user                 # noqa: F401 -> register models
import app.models.task                 # noqa: F401 -> register models

# Test DB URL (now reads from .env.test file)
TEST_DB_URL = os.getenv(
    "TEST_DATABASE_URL"
)

# Build an engine/session JUST for tests
engine = create_engine(TEST_DB_URL, pool_pre_ping=True, future=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    """Create all tables once for the test database, drop when session ends."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_tables():
    """
    Truncate tables before each test so tests don't leak data.
    MySQL needs FK checks toggled when truncating multi-FK graphs.
    """
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        # Truncate in child->parent order to be explicit
        conn.execute(text("TRUNCATE TABLE tasks"))
        conn.execute(text("TRUNCATE TABLE users"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        conn.commit()
    yield


@pytest.fixture
def db_session():
    """Yield a fresh ORM session per test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# ---- FastAPI TestClient, overriding get_db dependency ----
from fastapi.testclient import TestClient


@pytest.fixture
def client(db_session):
    # Override the app's get_db dependency to use the testing session
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    # Import the function to override
    from app.core.db import get_db  # original dependency
    fastapi_app.dependency_overrides[get_db] = _get_db_override

    with TestClient(fastapi_app) as c:
        yield c

    # Clean up override
    fastapi_app.dependency_overrides.clear()
