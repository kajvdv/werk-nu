from __future__ import annotations
import uuid
from datetime import datetime

import pytest
from freezegun import freeze_time
from httpx import Response
from fastapi.testclient import TestClient
from sqlalchemy import Connection

from backend.schemas.vacancy import VacancyCreate, VacancyPublic, VacancyDB
from backend.schemas.user import UserDB, UserCreate
from backend.schemas.applicant import ApplicantPublic
from backend.schemas.organization import OrganizationDB, OrganizationCreate
from backend.schemas.token import TokenCreate
from backend.services.auth import AuthService
from backend.services.user import UserService
from backend.services.vacancy import VacancyService
from backend.services.organization import OrganizationService


class TestVacancies:
    @pytest.fixture(autouse=True)
    def register_entities(self,
            conn: Connection,
            organization_service: OrganizationService,
            user_service: UserService
    ):
        organization_service.create_organization(OrganizationCreate(
            name="org 1",
            email="org@org1.com",
            password="password",
        ), active=True)

        organization_service.create_organization(OrganizationCreate(
            name="org 2",
            email="org@org2.com",
            password="password",
        ), active=True)

        user_service.create_user(UserCreate(
            name="John doe",
            email="john@doe.com",
            password="password"
        ), active=True)

        conn.commit()

    @pytest.fixture(autouse=True)
    def create_vacancies(self, register_entities, vacancy_service: VacancyService):
        with freeze_time(datetime(2026, 4, 12)):
            vacancy_service.create_vacancy(VacancyCreate(
                title="test vacancy",
                organization="org 1",
                location="test location",
                availability="test"
            ), public_organization_id=uuid.UUID("00000000-0000-4000-8000-000000000001"))

            vacancy_service.create_vacancy(VacancyCreate(
                title="test vacancy 2",
                organization="org 2",
                location="test location",
                availability="test"
            ), public_organization_id=uuid.UUID("00000000-0000-4000-8000-000000000002"))

            vacancy_service.conn.commit()

    @pytest.fixture
    def user(self, fastapi_app):
        client = TestClient(fastapi_app)
        access_token, *_ = client.post("/token", data={
            "username": "john@doe.com",
            "password": "password"
        }).json().values()
        client.headers['Authorization'] = f"Bearer {access_token}"
        return client

    @pytest.fixture
    def employer(self, fastapi_app):
        client = TestClient(fastapi_app)
        access_token, *_ = client.post("/token", data={
            "username": "org@org1.com",
            "password": "password"
        }).json().values()
        client.headers['Authorization'] = f"Bearer {access_token}"
        return client
    
    @pytest.fixture
    def other_employer(self, fastapi_app):
        client = TestClient(fastapi_app)
        access_token, *_ = client.post("/token", data={
            "username": "org@org2.com",
            "password": "password"
        }).json().values()
        client.headers['Authorization'] = f"Bearer {access_token}"
        return client

    def test_user_gets_all_vacancies(self, user):
        vacancies = user.get("/vacancies").json()
        assert vacancies == [{
            'availability': 'test',
            'closed': False,
            'id': '00000000-0000-4000-8000-000000000004',
            'location': 'test location',
            'newVacancy': False,
            'organization': 'org 1',
            'organization_id': '00000000-0000-4000-8000-000000000001',
            'title': 'test vacancy',
        },
        {
            'availability': 'test',
            'closed': False,
            'id': '00000000-0000-4000-8000-000000000005',
            'location': 'test location',
            'newVacancy': False,
            'organization': 'org 2',
            'organization_id': '00000000-0000-4000-8000-000000000002',
            'title': 'test vacancy 2',
        }]
    
    def test_apply_to_vacancy(self, user):
        application = user.post("/vacancies/00000000-0000-4000-8000-000000000004/applications").json()
        assert application == {
            'user': {
                'email': 'john@doe.com',
                'id': '00000000-0000-4000-8000-000000000003',
                'name': 'John doe',
            },
            'vacancy': {
                'availability': 'test',
                'closed': False,
                'id': '00000000-0000-4000-8000-000000000004',
                'location': 'test location',
                'newVacancy': False,
                'organization': 'org 1',
                'organization_id': '00000000-0000-4000-8000-000000000001',
                'title': 'test vacancy',
            },
        }

    def test_other_employer_cant_apply(self, other_employer):
        ...
    
    def test_employer_and_user_get_the_same_vacancies(self, employer, user):
        url = "/vacancies"
        assert employer.get(url).json() == user.get(url).json()
    
    def test_get_own_vacancies(self, employer):
        vacancies = employer.get("/vacancies/me").json()
        assert vacancies == [
            {
                'availability': 'test',
                'closed': False,
                'id': '00000000-0000-4000-8000-000000000004',
                'location': 'test location',
                'newVacancy': False,
                'organization': 'org 1',
                'organization_id': '00000000-0000-4000-8000-000000000001',
                'title': 'test vacancy',
                'created_at': datetime(2026, 4, 12).isoformat(),
                'applyCount': 0
            },
        ]

    def test_apply_count_rises_after_user_applies(self, employer, user):
        user.post("/vacancies/00000000-0000-4000-8000-000000000004/applications")
        apply_count = employer.get("/vacancies/me").json()[0]['applyCount']
        assert apply_count == 1

    def test_user_can_only_apply_once_on_vacancy(self):
        ...

    def test_employer_deletes_vacancy(self, employer: TestClient):
        employer.delete("/vacancies/00000000-0000-4000-8000-000000000004")
        vacancies = employer.get("/vacancies/me").json()
        assert vacancies == []

    def test_other_employer_cant_delete_vacancy(self, other_employer: TestClient):
        response = other_employer.delete("/vacancies/00000000-0000-4000-8000-000000000004")
        assert response.status_code == 401

    def test_user_gets_404_on_requestion_own_vacancies(self, user: TestClient):
        response = user.get("/vacancies/me")
        assert response.status_code == 404


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