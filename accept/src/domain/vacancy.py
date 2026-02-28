

from api.schemas.vacancy import VacancyPublic
from client import App

from domain.application import Application


class Vacancy:
    def __init__(self, employer_client: App, vacancy: VacancyPublic) -> None:
        self.vacancy = vacancy
        self.employer_client = employer_client
    
    def received_applications(self):
        public_schemas = self.employer_client.get_applicants(
            vacancy=self.vacancy
        )
        return [Application.from_public_schema(schema) for schema in public_schemas]
