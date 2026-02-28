from typing import Self

from api.schemas.applicant import ApplicantPublic


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
        ...
