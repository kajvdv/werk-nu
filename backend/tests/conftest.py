from __future__ import annotations
from typing import TYPE_CHECKING
import itertools
import os
import uuid

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.schemas.user import UserCreate, UserDB
from backend.schemas.organization import OrganizationCreate
from backend.schemas.vacancy import VacancyCreate
from backend.schemas.token import TokenCreate

if TYPE_CHECKING:
    from backend.services.auth import AuthService
    from backend.services.user import UserService


@pytest.fixture(autouse=True, scope="class")
def load_env_vars():
    from dotenv import load_dotenv
    load_dotenv(".env.test")


@pytest.fixture(name="conn", scope="class")
def connection_fixture():
    from backend.database import get_conn
    for conn in get_conn():
        yield conn


@pytest.fixture(autouse=True, scope="class")
def resetdb(conn):
    from backend.cli import resetdb
    resetdb()


@pytest.fixture(scope="class")
def fastapi_app():
    from backend.main import app
    return app


@pytest.fixture(scope="class")
def client(fastapi_app):
    BACKEND_URL = os.environ['BACKEND_URL']
    return TestClient(
        fastapi_app,
        base_url=BACKEND_URL
    )


@pytest.fixture(scope="class")
def uuid_factory(fastapi_app):
    from backend.dependencies import get_uuid_factory
    counter = itertools.count(1)
    override = lambda: uuid.UUID(int=next(counter), version=4)
    fastapi_app.dependency_overrides[get_uuid_factory] = lambda: override
    return override


@pytest.fixture(scope="class")
def mail_service():
    from backend.services.mail import MailService
    return MailService()


@pytest.fixture(scope="class")
def auth_service(conn, mail_service, uuid_factory):
    from backend.services.auth import AuthService
    return AuthService(conn, mail_service, uuid_factory)


@pytest.fixture(scope="class")
def user_service(conn, auth_service):
    from backend.services.user import UserService
    return UserService(conn, auth_service)


@pytest.fixture(scope="class")
def organization_service(conn, auth_service):
    from backend.services.organization import OrganizationService
    return OrganizationService(conn, auth_service)


@pytest.fixture(scope="class")
def vacancy_service(conn, organization_service, uuid_factory):
    from backend.services.vacancy import VacancyService
    return VacancyService(conn, organization_service, uuid_factory)


@pytest.fixture(scope="class")
def user_create():
    return UserCreate(
        name="test user",
        email="test@test.com",
        password="password"
    )


@pytest.fixture(scope="class")
def user_db(
        user_service: UserService,
        auth_service: AuthService,
        user_create: UserCreate,
):
    user_db = user_service.create_user(user_create)
    code = auth_service.get_code_for_user(user_db.id)
    assert code
    auth_service.activate_account(code)
    user_service.conn.commit()
    return user_db


@pytest.fixture(scope="class")
def organization_db(organization_service):
    organization_create = OrganizationCreate(
        name="test org",
        email="test@org.com",
        password="password"
    )
    organization_db = organization_service.create_organization(organization_create)
    organization_service.conn.commit()
    return organization_db


@pytest.fixture
def user_client(
        fastapi_app: FastAPI,
        user_db: UserDB,
        auth_service: AuthService
):
    client = TestClient(fastapi_app)
    token_create = TokenCreate.model_validate({
        "sub": user_db.name,
        "email": user_db.email,
        "name": user_db.name,
        "id": user_db.public_id,
        "entity_type": "user",
        "active": True
    }, by_name=True)
    token = auth_service.create_access_token(token_create)
    client.headers['Authorization'] = f"Bearer {token}"
    return client


@pytest.fixture
def employer_client(
        fastapi_app: FastAPI,
        organization_db,
        auth_service: AuthService
):
    client = TestClient(fastapi_app)
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
    return client



@pytest.fixture(scope="class")
def vacancy_create(organization_db):
    return VacancyCreate(
        title="test vacancy",
    )


@pytest.fixture(scope="class")
def vacancy_db(vacancy_create, organization_db, vacancy_service):
    vacancy_db = vacancy_service.create_vacancy(vacancy_create, organization_db.public_id)
    vacancy_service.conn.commit()
    return vacancy_db