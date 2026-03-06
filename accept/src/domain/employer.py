from typing import Self

from api.schemas.vacancy import VacancyCreate
from domain.users import User
from domain.vacancy import Vacancy


class Employer(User):
    _employers: dict[str, Self] = {}
    def __init__(self, name) -> None:
        self.name = name
        super().__init__()

    @classmethod
    def from_name(cls, name: str):
        if name in cls._employers:
            return cls._employers[name]
        else:
            employer = cls(name)
            cls._employers[name] = employer
            return employer

    def post_vacancy(self, vacancy: VacancyCreate) -> Vacancy:
        public_schema = self.app.post_vacancy(self.name, vacancy)
        return Vacancy(
            employer_client=self.app,
            vacancy=public_schema
        )
    