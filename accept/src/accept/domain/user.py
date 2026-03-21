from abc import ABC, abstractmethod

from backend.schemas.message import MessageCreate

from accept.mocks.mail import MailpitSpy
from accept.drivers import Driver


class User(ABC):
    def __init__(self, driver: Driver) -> None:
        self.driver = driver
        self.mail = MailpitSpy()
        self._messages = []
        self.email: str = ""
        self.password: str = ""

    def activate_account(self):
        activation_url = self.mail.get_last_mail()['Snippet']
        self.driver.activate_account(activation_url.split("/")[-1])

    def login(self):
        self.driver.login(self.email, self.password)
    
    def send_message(self, to: str, message: MessageCreate):
        self.driver.send_message(to, message)

    @abstractmethod
    def register(self):
        ...

    @property
    def messages(self):
        messages = self.driver.get_messages()
        return [m.text for m in messages]