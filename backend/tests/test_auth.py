from __future__ import annotations
from typing import TYPE_CHECKING

import pytest
from fastapi import FastAPI

from api.schemas.token import TokenCreate
from api.schemas.user import UserDB, UserCreate
from api.services.mail import Mail, MailService
from client import App

from mocks.mail import MailServiceMock

if TYPE_CHECKING:
    from api.services.auth import AuthService


class TestAuthUser:
    @pytest.fixture
    def token_create(self, user_db: UserDB):
        return TokenCreate.model_validate({
            "sub": user_db.name,
            "email": user_db.email,
            "name": user_db.name,
            "id": user_db.public_id,
            "entity_type": "user",
            "active": True
        }, by_name=True)
    
    def test_user_can_login(self, user_db, auth_service):
        success = auth_service.login(user_db.email, "password")
        assert success

    def test_access_token_data_contains_entity_type(self, user_db, auth_service, token_create):
        auth_service.login(user_db.email, "password")
        token = auth_service.create_access_token(token_create)
        assert "entity_type" in auth_service.decode_token(token)


class TestAuthOrg:

    def test_only_org_can_get_its_applications(self):
        ...


class TestRegister:
    @pytest.fixture
    def mail_service(self):
        return MailServiceMock()
    
    @pytest.fixture(autouse=True)
    def mock_mail_service(self, fastapi_app: FastAPI, mail_service: MailServiceMock):
        from api.dependencies import get_mail_service
        fastapi_app.dependency_overrides[get_mail_service] = lambda: mail_service
    
    def test_register_applicant(self,
            mail_service: MailServiceMock,
            auth_service: AuthService,
            app: App,
            user_create: UserCreate,
    ):
        app.register_user(user_create)
        activation_link = mail_service.get_last_mail().content
        code = activation_link.split("/")[-1]
        app.activate_account(code)
        auth_user_db = auth_service.get_auth_user(user_create.email)
        assert auth_user_db.active
