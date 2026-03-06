from typing import Self

import httpx

from api.schemas.message import MessageCreate
from client import App


class User:
    def __init__(self) -> None:
        self.app = App(client=httpx.Client(base_url="http://localhost:8000")) # Every user has their own app/client
        self._messages = []
        self.user_id = 1
    
    def send_message(self, to: str, message: MessageCreate):
        self.app.send_message(to, message)

    @property
    def messages(self):
        messages = self.app.get_messages(self.user_id)
        return [m["text"] for m in messages]
