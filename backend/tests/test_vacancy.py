import pytest
from fastapi import FastAPI

from client import App
from api.schemas.vacancy import VacancyCreate, VacancyPublic
from api.schemas.user import UserCreate, UserPublic
from api.schemas.organization import OrganizationCreate


class TestApplyToVacancy:

    @pytest.fixture(autouse=True)
    def dependency_inject_fastapi(self, fastapi_app: FastAPI, user_db):
        from api.dependencies import get_current_user
        def get_current_user_override():
            return UserPublic.model_validate({
                **user_db.model_dump()
            })
        
        fastapi_app.dependency_overrides[get_current_user] = get_current_user_override


    def test_post_new_vacancy(self,
            app: App,
            vacancy_create,
            organization_db
    ):
        vacancy = app.post_vacancy(organization_db.name, vacancy_create)
        assert vacancy.title == "test vacancy"

    
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
