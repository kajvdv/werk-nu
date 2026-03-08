from __future__ import annotations
from typing import TYPE_CHECKING

from api.schemas.applicant import ApplicantPublic
from api.schemas.message import MessageCreate

if TYPE_CHECKING:
    from domain.vacancy import Vacancy
    from client import App


class Application:

    def __init__(self,
            application: ApplicantPublic,
            employer_client: App,
            user_client: App,
    ) -> None:
        self.application = application
        self.employer_client = employer_client
        self.user_client = user_client

    def in_vacancy(self, vacancy: Vacancy) -> bool:
        for received_application in vacancy.received_applications():
            if received_application == self.application:
                return True
        return False
    
    def send_message(self, text: str):
        message = MessageCreate.model_validate({
            "text": text,
            "recipient_id": self.application.user.id
        })
        self.employer_client.send_message(self.application.user.id, message)
