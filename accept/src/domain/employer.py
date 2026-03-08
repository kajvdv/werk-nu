from typing import Self

from api.schemas.vacancy import VacancyCreate
from api.schemas.organization import OrganizationCreate
from domain.users import User
from domain.vacancy import Vacancy


class Employer(User):
    def __init__(
            self,
            name: str,
            email: str,
    ) -> None:
        self.name = name
        super().__init__()
        pw = "password"
        self.app.register_organization(OrganizationCreate(
            name="Test org",
            email=email,
            password=pw
        ))
        self.app.login(email, pw)

    def create_vacancy(self, vacancy: VacancyCreate) -> Vacancy:
        public_schema = self.app.post_vacancy(vacancy)
        return Vacancy(
            employer_client=self.app,
            vacancy=public_schema
        )
    