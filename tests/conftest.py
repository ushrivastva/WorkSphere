import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.modules.users.models import User # ---> register model metadata

@pytest.fixture
def db_engine():
    engine = create_engine(settings.test_database_url)

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(
        bind=db_engine,
        autocommit=False,
        autoflush=False
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()