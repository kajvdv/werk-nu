import json

import httpx

from api.schemas.vacancy import VacancyCreate, VacancyPublic
from api.schemas.applicant import ApplicantPublic
from api.schemas.user import UserCreate
from api.schemas.organization import OrganizationCreate
from api.schemas.message import MessageCreate


class App:
    def __init__(self, client: httpx.Client) -> None:
        self.client = client

    def register_organization(self, organization_data: OrganizationCreate):
        response = self.client.post("/organizations", json=organization_data.model_dump())
        assert response.status_code == 201, response.json()
        return response.json()

    def register_user(self, user_data: UserCreate):
        response = self.client.post("/users", json=user_data.model_dump())
        assert response.status_code == 201
        return response.json()

    def login(self, email: str, password: str):
        response = self.client.post("/token", data={
            "username": email,
            "password": password,
        })
        assert response.status_code == 200
        access_token = response.json()['access_token']
        self.client.headers['Authorization'] = f"Bearer {access_token}"
        return response.json()
    
    def post_vacancy(self, vacancy: VacancyCreate) -> VacancyPublic:
        response = self.client.post(
            url=f"/me/vacancies",
            json=json.loads(
                vacancy.model_dump_json()
            )
        )
        assert response.status_code == 200
        return VacancyPublic.model_validate(response.json(), by_name=True)

    def post_application(self, vacancy: VacancyPublic):
        response = self.client.post(
            url=f"/{vacancy.organization_id}/vacancies/{vacancy.id}/applications",
        )
        assert response.status_code == 200
        return ApplicantPublic.model_validate(response.json(), by_name=True)

    def get_applicants(self, vacancy: VacancyPublic) -> list[ApplicantPublic]:
        response = self.client.get(
            url=f"/{vacancy.organization_id}/vacancies/{vacancy.id}/applications"
        )
        assert response.status_code == 200
        return [ApplicantPublic.model_validate(a, by_name=True) for a in response.json()]
    
    def get_messages(self):
        response = self.client.get(f"/users/me/messages")
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
