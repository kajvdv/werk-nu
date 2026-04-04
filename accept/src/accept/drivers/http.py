import os

import httpx

from backend.schemas.vacancy import VacancyCreate, VacancyPublic
from backend.schemas.applicant import ApplicantPublic
from backend.schemas.user import UserCreate
from backend.schemas.organization import OrganizationCreate
from backend.schemas.message import MessageCreate, MessagePublic


class HttpDriver:
    def __init__(self) -> None:
        BACKEND_URL = os.environ["BACKEND_URL"]
        self.client =  httpx.Client(base_url=BACKEND_URL)

    def register_organization(self, organization_data: OrganizationCreate):
        response = self.client.post("/organizations", json=organization_data.model_dump())
        assert response.status_code == 201, response.json()
        return response.json()

    def register_user(self, user_data: UserCreate):
        response = self.client.post("/users", json=user_data.model_dump())
        assert response.status_code == 201
        return response.json()

    def activate_account(self, code):
        response = self.client.get(f"/register/activate/{code}")
        assert response.status_code == 204, response.reason_phrase
        return

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
            url=f"/vacancies",
            json=vacancy.model_dump()
        )
        assert response.status_code == 201
        return VacancyPublic.model_validate(response.json(), by_name=True)

    def post_application(self, vacancy: VacancyPublic):
        response = self.client.post(
            url=f"/vacancies/{vacancy.id}/applications",
        )
        assert response.status_code == 200
        return ApplicantPublic.model_validate(response.json(), by_name=True)

    def get_applicants(self, vacancy: VacancyPublic) -> list[ApplicantPublic]:
        response = self.client.get(
            url=f"/vacancies/{vacancy.id}/applications"
        )
        assert response.status_code == 200
        return [ApplicantPublic.model_validate(a, by_name=True) for a in response.json()]
    
    def get_messages(self) -> list[MessagePublic]:
        response = self.client.get(f"/users/me/messages")
        assert response.status_code == 200
        return [MessagePublic.model_validate(m) for m in response.json()]
    
    def send_message(self, user_id, message: MessageCreate):
        response = self.client.post(
            url=f"/users/{user_id}/messages",
            json=message.model_dump()
        )
        assert response.status_code == 200
