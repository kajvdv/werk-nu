from typing import Self

from api.schemas import VacancyCreate

from domain.app import App
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
        return Application()


class Employer(User):
    def __init__(self, app: App) -> None:
        super().__init__(app)

    def post_vacancy(self, vacancy: VacancyCreate) -> Vacancy:
        return Vacancy()