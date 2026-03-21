from __future__ import annotations
from typing import TYPE_CHECKING
import os

import pytest
from fastapi.testclient import TestClient

from backend.schemas.user import UserCreate
from backend.schemas.organization import OrganizationCreate
from backend.schemas.vacancy import VacancyCreate

if TYPE_CHECKING:
    from backend.services.auth import AuthService
    from backend.services.user import UserService


@pytest.fixture(autouse=True)
def load_env_vars():
    from dotenv import load_dotenv
    load_dotenv(".env.test")


@pytest.fixture(name="conn")
def connection_fixture():
    from backend.database import get_conn
    for conn in get_conn():
        yield conn


@pytest.fixture(autouse=True)
def resetdb(conn):
    from backend.cli import resetdb
    resetdb()


@pytest.fixture
def fastapi_app():
    from backend.main import app
    return app


@pytest.fixture
def client(fastapi_app):
    BACKEND_URL = os.environ['BACKEND_URL']
    return TestClient(
        fastapi_app,
        base_url=BACKEND_URL
    )


@pytest.fixture
def mail_service():
    from backend.services.mail import MailService
    return MailService()


@pytest.fixture
def auth_service(conn, mail_service):
    from backend.services.auth import AuthService
    return AuthService(conn, mail_service)


@pytest.fixture
def user_service(conn, auth_service):
    from backend.services.user import UserService
    return UserService(conn, auth_service)


@pytest.fixture
def organization_service(conn, auth_service):
    from backend.services.organization import OrganizationService
    return OrganizationService(conn, auth_service)


@pytest.fixture
def vacancy_service(conn, organization_service):
    from backend.services.vacancy import VacancyService
    return VacancyService(conn, organization_service)


@pytest.fixture
def user_create():
    return UserCreate(
        name="test user",
        email="test@test.com",
        password="password"
    )


@pytest.fixture
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


@pytest.fixture
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
def vacancy_create(organization_db):
    return VacancyCreate(
        title="test vacancy",
    )


@pytest.fixture
def vacancy_db(vacancy_create, organization_db, vacancy_service):
    vacancy_db = vacancy_service.create_vacancy(vacancy_create, organization_db.public_id)
    vacancy_service.conn.commit()
    return vacancy_db