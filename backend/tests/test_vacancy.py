from __future__ import annotations

import pytest
from httpx import Response
from fastapi.testclient import TestClient

from backend.schemas.vacancy import VacancyCreate, VacancyPublic, VacancyDB
from backend.schemas.user import UserDB
from backend.schemas.applicant import ApplicantPublic
from backend.schemas.organization import OrganizationDB
from backend.schemas.token import TokenCreate
from backend.services.auth import AuthService
from backend.services.vacancy import VacancyService


class TestUseVacancy:
    @pytest.fixture(scope="class")
    def vacancy_create(self):
        return VacancyCreate(
            title="test vacancy",
            organization="test org",
            location="ergens",
            availability="niet",
        )

    @pytest.fixture(autouse=True, scope="class")
    def auth_client(self,
            client: TestClient,
            organization_db: OrganizationDB,
            auth_service: AuthService
    ):
        token_create = TokenCreate.model_validate({
            "sub": organization_db.name,
            "email": organization_db.email,
            "name": organization_db.name,
            "id": organization_db.public_id,
            "entity_type": "organization",
            "active": True
        }, by_name=True)
        token = auth_service.create_access_token(token_create)
        client.headers['Authorization'] = f"Bearer {token}"

    
    @pytest.fixture(scope="class")
    def post_vacancy_response(self,
            client: TestClient,
            vacancy_create: VacancyCreate,
    ):
        response = client.post(
            url=f"/vacancies",
            json=vacancy_create.model_dump()
        )
        return response


    def test_post_response_is_201(self,
            post_vacancy_response: Response,
    ):
        assert post_vacancy_response.status_code == 201

    def test_title_is_correct(self, post_vacancy_response: Response):
        vacancy = VacancyPublic.model_validate(
            post_vacancy_response.json(),
            by_name=True,
        )
        assert vacancy.title == "test vacancy"

    
    def test_get_all_vacancies(self, client: TestClient):
        response = client.get("/vacancies")
        assert response.status_code == 200
        assert response.json() == [
            {
                "title": "test vacancy",
                "organization_id": "00000000-0000-4000-8000-000000000001",
                "id": "00000000-0000-4000-8000-000000000002",
                "organization": "test org",
                "location": "ergens",
                "availability": "niet",
                "newVacancy": False,
                "closed": False,
            },
        ]

    
    def test_apply_to_vacancy_with_service(self,
            vacancy_service: VacancyService,
            vacancy_db: VacancyDB,
            user_db: UserDB,
    ):
        vacancy_service.apply(user_db, vacancy_db)
        applications = vacancy_service.get_applications(vacancy_db)

        assert len(applications) == 1
        assert applications[0].user.name == "test user"


    # def test_apply_to_vacancy_through_endpoint(self, fastapi_app, user_db, vacancy_db):
    #     # vacancy_public = VacancyPublic.model_validate({
    #     #     "organization_id": vacancy_db.public_id,
    #     #     **vacancy_db.model_dump(exclude={"organization_id"}),
    #     # })
    #     client = TestClient(fastapi_app)
    #     token = client.post("/token", data={
    #         "username": "test@test.com",
    #         "password": "password"
    #     })
    #     client.headers['Authorization'] = f"Bearer {token.json()['access_token']}"
    #     response = client.post(
    #         url=f"/vacancies/{vacancy_db.public_id}/applications",
    #     )
    #     application_public = ApplicantPublic.model_validate(response.json(), by_name=True)

    #     assert application_public.user.name == "test user"


# class TestApplyVacancy:
#     @pytest.fixture
#     def vacancy(self,
#             employer_client: TestClient
#     ):
#         data = VacancyCreate(title="test vacancy")
#         return VacancyPublic.model_validate(
#             employer_client.post("/vacancies", json=data.model_dump()).json(),
#             by_name=True
#         )
    
#     def test_user_gets_vacancy(self,
#             user_client: TestClient,
#             vacancy: VacancyPublic,
#     ):
#         vacancies = user_client.get("/vacancies").json()
#         assert vacancy.model_dump() in vacancies
        
#     def test_user_succesfully_applies_to_vacancy(self,
#             user_client: TestClient,
#             employer_client: TestClient,
#             vacancy: VacancyPublic,
#     ): 
#         url = f"/vacancies/{vacancy.id}/applications"
#         application = user_client.post(url).json()
#         applications = employer_client.get(url).json()
#         assert application in applications