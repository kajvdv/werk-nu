from typing import Self

from domain.users import User
from domain.vacancy import Vacancy
from domain.application import Application


class Applicant(User):
    _applicants: dict[str, Self] = {}
    
    @classmethod
    def from_id(cls, id: str):
        if id in cls._applicants:
            return cls._applicants[id]
        else:
            applicant = cls()
            cls._applicants[id] = applicant
            return applicant
    
    def apply(self, vacancy: Vacancy) -> Application:
        public_schema = self.app.post_application(vacancy.vacancy)
        return Application.from_public_schema(
            application=public_schema
        )