from typing import Self

from api.schemas.vacancy import VacancyCreate

from client import App
from domain.vacancy import Vacancy
from domain.application import Application


class User:
    def __init__(self, app: App) -> None:
        self.app = app
        self.messages = []
    
    def send_message(self, to: Self, text: str):
        ...


class Applicant(User):
    def __init__(self, app: App) -> None:
        super().__init__(app)

    def apply(self, vacancy: Vacancy) -> Application:
        public_schema = self.app.post_application(vacancy.vacancy)
        return Application.from_public_schema(
            application=public_schema
        )


class Employer(User):
    def __init__(self, app: App) -> None:
        super().__init__(app)
        self.name = "test employer"

    def post_vacancy(self, vacancy: VacancyCreate) -> Vacancy:
        public_schema = self.app.post_vacancy(self.name, vacancy)
        return Vacancy(
            employer_client=self.app,
            vacancy=public_schema
        )