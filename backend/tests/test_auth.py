from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.schemas.token import TokenCreate
from backend.schemas.user import UserDB, UserCreate
from backend.services.auth import AuthService

from mocks.mail import MailServiceMock


class TestAuthUser:
    @pytest.fixture(scope="class")
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
    @pytest.fixture(scope="class")
    def mail_service(self):
        return MailServiceMock()
    
    @pytest.fixture(autouse=True)
    def mock_mail_service(self, fastapi_app: FastAPI, mail_service: MailServiceMock):
        from backend.dependencies import get_mail_service
        fastapi_app.dependency_overrides[get_mail_service] = lambda: mail_service
    
    def test_register_applicant(self,
            mail_service: MailServiceMock,
            auth_service: AuthService,
            client: TestClient,
            user_create: UserCreate,
    ):
        response = client.post("/users", json=user_create.model_dump())
        assert response.status_code == 201

        activation_link = mail_service.get_last_mail().content
        code = activation_link.split("/")[-1]
        
        response = client.post(f"/register/activate/{code}")
        assert response.status_code == 204, response.reason_phrase

        auth_user_db = auth_service.get_auth_user(user_create.email)
        assert auth_user_db.active

    def test_activate_user(self,
            client: TestClient,
            user_create,
            user_service,
            auth_service
    ):
        user_db = user_service.create_user(user_create)
        code = auth_service.get_code_for_user(user_db.id)
        user_service.conn.commit()
        response = client.post(f"/register/activate/{code}")
        assert response.status_code == 204, response.reason_phrase
