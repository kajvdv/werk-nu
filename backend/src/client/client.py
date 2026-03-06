import json

import httpx

from api.schemas.vacancy import VacancyCreate, VacancyPublic
from api.schemas.applicant import ApplicantPublic
from api.schemas.message import MessageCreate


class App:
    def __init__(self) -> None:
        # TODO: Dependency inject client (for use Fastapi testclient)
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
    
    def get_messages(self, user_id):
        response = self.client.get(f"/users/{user_id}/messages")
        assert response.status_code == 200
        return response.json()
    
    def send_message(self, user_id, message: MessageCreate):
        response = self.client.post(
            url=f"/users/{user_id}/messages",
            json=json.loads(
                message.model_dump_json()
            )
        )
        assert response.status_code == 200
