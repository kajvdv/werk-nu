from __future__ import annotations
from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient

from backend.schemas.vacancy import VacancyCreate, VacancyPublic, VacancyDB
from backend.schemas.user import UserDB
from backend.schemas.applicant import ApplicantPublic
from backend.schemas.organization import OrganizationCreate, OrganizationDB
from backend.schemas.token import TokenCreate

if TYPE_CHECKING:
    from backend.services.auth import AuthService
    from backend.services.vacancy import VacancyService


class TestPostVacancy:

    @pytest.fixture(autouse=True)
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


    def test_post_new_vacancy(self,
            client: TestClient,
            vacancy_create: VacancyCreate,
    ):
        response = client.post(
            url=f"/me/vacancies",
            json=vacancy_create.model_dump()
        )
        assert response.status_code == 200
        vacancy = VacancyPublic.model_validate(response.json(), by_name=True)
        assert vacancy.title == "test vacancy"


class TestApply:

    @pytest.fixture(autouse=True)
    def auth_client(self,
            client: TestClient, 
            user_db: UserDB, 
            auth_service: AuthService,
    ):
        token_create = TokenCreate.model_validate({
            "sub": user_db.name,
            "email": user_db.email,
            "name": user_db.name,
            "id": user_db.public_id,
            "entity_type": "organization",
            "active": True
        }, by_name=True)
        token = auth_service.create_access_token(token_create)
        client.headers['Authorization'] = f"Bearer {token}"
    
    def test_apply_to_vacancy_with_service(self,
            vacancy_service: VacancyService,
            vacancy_db: VacancyDB,
            user_db: UserDB,
    ):

        vacancy_service.apply(user_db, vacancy_db)
        applications = vacancy_service.get_applications(vacancy_db)

        assert len(applications) == 1
        assert applications[0].user.name == "test user"


    def test_apply_to_vacancy_through_endpoint(self, client, user_db, vacancy_db):
        vacancy_public = VacancyPublic.model_validate({
            "organization_id": vacancy_db.public_id,
            **vacancy_db.model_dump(exclude={"organization_id"}),
        })
        response = client.post(
            url=f"/{vacancy_public.organization_id}/vacancies/{vacancy_public.id}/applications",
        )
        application_public = ApplicantPublic.model_validate(response.json(), by_name=True)

        assert application_public.user.name == "test user"
