import warnings

from starlette.exceptions import StarletteDeprecationWarning

warnings.filterwarnings("ignore", category=StarletteDeprecationWarning)

import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.core.database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    database = TestSessionLocal()
    try:
        yield database
    finally:
        database.close()


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    user_resp = client.post("/api/auth/registro", json={
        "nombre": "Admin",
        "email": "admin@test.com",
        "password": "testpass",
    }).json()
    db = TestSessionLocal()
    user = db.query(type('Usuario', (object,), {'__tablename__': 'usuario'})) if False else None
    from backend.models.models import Usuario as UsuarioModel
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == user_resp["id"]).first()
    usuario.es_admin = True
    db.commit()
    db.close()

    resp = client.post("/api/auth/login", json={
        "email": "admin@test.com",
        "password": "testpass",
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_data(client):
    user_resp = client.post("/api/auth/registro", json={
        "nombre": "Normal User",
        "email": "normal@test.com",
        "password": "testpass",
    }).json()
    resp = client.post("/api/auth/login", json={
        "email": "normal@test.com",
        "password": "testpass",
    })
    token = resp.json()["access_token"]
    return {
        "headers": {"Authorization": f"Bearer {token}"},
        "user_id": user_resp["id"],
    }


@pytest.fixture
def admin_data(client):
    user_resp = client.post("/api/auth/registro", json={
        "nombre": "Admin",
        "email": "admin@test.com",
        "password": "testpass",
    }).json()
    db = TestSessionLocal()
    from backend.models.models import Usuario as UsuarioModel
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == user_resp["id"]).first()
    usuario.es_admin = True
    db.commit()
    db.close()

    resp = client.post("/api/auth/login", json={
        "email": "admin@test.com",
        "password": "testpass",
    })
    token = resp.json()["access_token"]
    return {
        "headers": {"Authorization": f"Bearer {token}"},
        "user_id": user_resp["id"],
    }
