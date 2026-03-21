import pytest
from fastapi.testclient import TestClient

from backend.schemas.message import MessageCreate
from backend.schemas.user import UserDB


@pytest.fixture
def message_create():
    return MessageCreate(
        text="This is a test message."
    )


class TestUserMessages:
    @pytest.fixture(autouse=True)
    def login_user(self, client, user_db, user_create):
        response = client.post("/token", data={
            "username": user_create.email,
            "password": user_create.password,
        })
        assert response.status_code == 200
        access_token = response.json()['access_token']
        client.headers['Authorization'] = f"Bearer {access_token}"

    def test_user_can_get_messeges(self, client):
        response = client.get(f"/users/me/messages")
        assert response.status_code == 200

    def test_cannot_post_message_to_self(self,
            client: TestClient,
            user_db: UserDB,
            message_create: MessageCreate,
    ):
        response = client.post(
            url=f"/users/{user_db.public_id}/messages",
            json=message_create.model_dump()
        )
        assert response.status_code == 400, response.text
