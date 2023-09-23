import os
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database.database import Base, get_db
from ..main import app

TEST_DATABASE_URL = os.getenv("MYSQL_TEST_ENDPOINT")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {"Hello": "World"}


class TestRoom:
    def test_create_room_success(self):
        response = client.post(
            "/room/create",
            json={"duration": "P3D"},
        )
        assert response.status_code == 200, response.text
        assert len(response.json()["ref_code"]) == 6

        created_at = datetime.fromisoformat(response.json()["created_at"])
        close_at = datetime.fromisoformat(response.json()["close_at"])
        assert close_at - created_at == timedelta(days=3)

    def test_create_room_with_negative_duration_fail(self):
        response = client.post(
            "/room/create",
            json={"duration": "-P3D"},
        )
        assert response.status_code == 422, response.text

    def test_create_room_with_invalid_duration_fail(self):
        response = client.post(
            "/room/create",
            json={"duration": "P3D2H"},
        )
        assert response.status_code == 422, response.text

    def test_get_room_success(self):
        response = client.post(
            "/room/create",
            json={"duration": "P1D"},
        )
        ref_code = response.json()["ref_code"]

        response = client.get(f"/room/{ref_code}")
        assert response.status_code == 200, response.text

    def test_get_room_with_invalid_ref_code_fail(self):
        response = client.get(f"/room/invalid_ref_code")
        assert response.status_code == 404, response.text

    # TODO: close test
