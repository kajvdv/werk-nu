import pytest
from fastapi import FastAPI

from api.schemas.vacancy import VacancyCreate, VacancyPublic
from api.schemas.user import UserCreate, UserPublic
from api.schemas.organization import OrganizationCreate


class TestApplyToVacancy:

    @pytest.fixture
    def user_db(self, user_service):
        user_create = UserCreate(
            name="test user"
        )
        user_db = user_service.create_user(user_create)
        return user_db
    

    @pytest.fixture
    def organization_db(self, organization_service):
        organization_create = OrganizationCreate(
            name="test org"
        )
        organization_db = organization_service.create_organization(organization_create)
        return organization_db


    @pytest.fixture
    def vacancy_db(self, organization_db, vacancy_service):
        vacancy_create = VacancyCreate(
            title="test",
            organization_id=organization_db.public_id,
        )
        vacancy_db = vacancy_service.create_vacancy(vacancy_create)
        return vacancy_db
    
    
    @pytest.fixture(autouse=True)
    def dependency_inject_fastapi(self, fastapi_app: FastAPI, user_db):
        from api.deps import get_current_user
        def get_current_user_override():
            return UserPublic.model_validate({
                **user_db.model_dump()
            })
        
        fastapi_app.dependency_overrides[get_current_user] = get_current_user_override

    
    def test_apply_to_vacancy_with_service(self,
            vacancy_service,
            vacancy_db,
            user_db,
    ):

        vacancy_service.apply(user_db, vacancy_db)
        applications = vacancy_service.get_applications(vacancy_db)

        assert len(applications) == 1
        assert applications[0].user.name == "test user"
        # assert applications[0].vacancy.oraganization == "test org"


    def test_apply_to_vacancy_with_app(self, app, vacancy_db):
        vacancy_public = VacancyPublic.model_validate({
            "organization_id": vacancy_db.public_id,
            **vacancy_db.model_dump(exclude={"organization_id"}),
        })
        application_public = app.post_application(vacancy_public)

        assert application_public.user.name == "test user"
