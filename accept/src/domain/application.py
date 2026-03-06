from typing import Self

from api.schemas.applicant import ApplicantPublic
from api.schemas.message import MessageCreate


class Application:

    applications: dict[tuple[str, str], Self] = {}
    def __init__(self, application: ApplicantPublic) -> None:
        self.application = application

    @classmethod
    def from_public_schema(cls, application: ApplicantPublic):
        key = (
            application.user.id,
            application.vacancy.id
        )
        if key in cls.applications:
            return cls.applications[key]
        else:
            value = cls(application)
            cls.applications[key] = value
            return value
    
    def send_message(self, text: str):
        from domain.employer import Employer
        from domain.applicant import Applicant
        name = self.application.vacancy.organization
        employer = Employer.from_name(name)
        message = MessageCreate.model_validate({
            "text": text,
            "recipient_id": self.application.user.id
        })
        recipient = Applicant.from_id(self.application.user.id)
        employer.send_message(recipient.user_id, message)
