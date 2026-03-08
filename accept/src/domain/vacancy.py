

from api.schemas.vacancy import VacancyPublic
from client import App


class Vacancy:
    def __init__(self, employer_client: App, vacancy: VacancyPublic) -> None:
        self.vacancy = vacancy
        self.employer_client = employer_client
    
    def received_applications(self):
        """Getting all the received applications using the employer client."""
        return self.employer_client.get_applicants(
            vacancy=self.vacancy
        )
