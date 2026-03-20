from typing import Self

import httpx

from domain.mail import MailpitSpy
from api.schemas.message import MessageCreate
from client import App


class User:
    def __init__(self) -> None:
        self.app = App(client=httpx.Client(base_url="http://localhost:8000")) # Every user has their own app/client
        self.mail = MailpitSpy()
        self._messages = []

    def _activate_account(self):
        activation_url = self.mail.get_last_mail()['Snippet']
        self.app.activate_account(activation_url.split("/")[-1])
    
    def send_message(self, to: str, message: MessageCreate):
        self.app.send_message(to, message)

    @property
    def messages(self):
        messages = self.app.get_messages()
        return [m["text"] for m in messages]
