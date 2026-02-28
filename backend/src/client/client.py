import json

import httpx

from api.schemas.vacancy import VacancyCreate, VacancyPublic
from api.schemas.applicant import ApplicantPublic


class App:
    def __init__(self) -> None:
        self.client = httpx.Client(base_url="http://localhost:8000")
    
    def post_vacancy(self, organization: str, vacancy: VacancyCreate) -> VacancyPublic:
        response = self.client.post(
            url=f"/{organization}/vacancies",
            json=json.loads(
                vacancy.model_dump_json()
            )
        )
        assert response.status_code == 200
        return VacancyPublic.model_validate(response.json())

    def post_application(self, vacancy: VacancyPublic):
        response = self.client.post(
            url=f"/{vacancy.organization}/vacancies/{vacancy.id}/applications",
        )
        assert response.status_code == 200
        return ApplicantPublic.model_validate(response.json())

    def get_applicants(self, vacancy: VacancyPublic) -> list[ApplicantPublic]:
        response = self.client.get(
            url=f"/{vacancy.organization}/vacancies/{vacancy.id}/applications"
        )
        assert response.status_code == 200
        return [ApplicantPublic.model_validate(a) for a in response.json()]