import os
from datetime import datetime, timedelta

import pytest
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
        response = client.get("/room/invalid_ref_code")
        assert response.status_code == 404, response.text

    # TODO: close test


class TestPerson:
    @pytest.fixture
    def room(self):
        response = client.post(
            "/room/create",
            json={"duration": "P1D"},
        )
        return response.json()

    def test_create_person_success(self, room):
        response = client.post(
            "/person/create",
            json={
                "name": "test",
                "room_id": room["id"],
            },
        )
        assert response.status_code == 200, response.text
        assert response.json()["name"] == "test"
        room_response = client.get(f"/room/{room['ref_code']}")
        assert len(room_response.json()["persons"]) == 1
        assert room_response.json()["persons"][0]["name"] == "test"

    def test_create_person_with_empty_name_fail(self, room):
        response = client.post(
            "/person/create",
            json={
                "name": "",
                "room_id": room["id"],
            },
        )
        assert response.status_code == 422, response.text

    def test_create_person_with_invalid_room_id_fail(self):
        response = client.post(
            "/person/create",
            json={
                "name": "test",
                "room_id": "invalid_room_id",
            },
        )
        assert response.status_code == 422, response.text

    # TODO: closed room fail


class TestContact:
    @pytest.fixture
    def room(self):
        response = client.post(
            "/room/create",
            json={"duration": "P1D"},
        )
        return response.json()

    @pytest.fixture
    def person(self, room):
        response = client.post(
            "/person/create",
            json={
                "name": "test",
                "room_id": room["id"],
            },
        )
        return response.json()

    @pytest.fixture
    def person_with_ref_code(self, room):
        response = client.post(
            "/person/create",
            json={
                "name": "test",
                "room_id": room["id"],
            },
        )
        return {"person": response.json(), "room_ref_code": room["ref_code"]}

    def test_create_contact_success(self, person_with_ref_code):
        response = client.post(
            "/contact/create",
            json={
                "person_id": person_with_ref_code["person"]["id"],
                "content": "test",
                "content_type": "github",
            },
        )
        assert response.status_code == 200, response.text
        assert response.json()["content"] == "test"
        assert response.json()["content_type"] == "github"

        room_response = client.get(f"/room/{person_with_ref_code['room_ref_code']}")
        assert len(room_response.json()["persons"][0]["contacts"]) == 1
        assert room_response.json()["persons"][0]["contacts"][0]["content"] == "test"

    def test_create_contact_with_empty_content_fail(self, person):
        response = client.post(
            "/contact/create",
            json={
                "person_id": person["id"],
                "content": "",
                "content_type": "github",
            },
        )
        assert response.status_code == 422, response.text

    def test_create_contact_with_invalid_person_id_fail(self):
        response = client.post(
            "/contact/create",
            json={
                "person_id": "invalid_person_id",
                "content": "test",
                "content_type": "github",
            },
        )
        assert response.status_code == 422, response.text

    def test_create_contact_with_invalid_content_type_fail(self, person):
        response = client.post(
            "/contact/create",
            json={
                "person_id": person["id"],
                "content": "test",
                "content_type": "invalid_content_type",
            },
        )
        assert response.status_code == 422, response.text
