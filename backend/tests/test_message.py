import pytest

from client import App

from api.schemas.message import MessageCreate


@pytest.fixture
def message_create():
    return MessageCreate(
        text="This is a test message."
    )


class TestUserMessages:

    @pytest.fixture(autouse=True)
    def login_user(self, app: App, user_db):
        app.login(user_db.email, "password")

    def test_user_can_get_messeges(self, app: App):
        app.get_messages()

    def test_cannot_post_message_to_self(self, app: App, user_db, message_create):
        with pytest.raises(Exception):
            app.send_message(user_id=user_db.public_id, message=message_create)
