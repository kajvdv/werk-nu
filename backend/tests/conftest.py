import pytest
from fastapi.testclient import TestClient

from api.schemas.user import UserCreate
from api.schemas.organization import OrganizationCreate
from api.schemas.vacancy import VacancyCreate


@pytest.fixture(autouse=True)
def load_env_vars():
    from dotenv import load_dotenv
    load_dotenv(".env.test")


@pytest.fixture(name="conn")
def connection_fixture():
    from api.database import get_conn
    for conn in get_conn():
        yield conn


@pytest.fixture(autouse=True)
def resetdb(conn):
    from cli.main import resetdb
    resetdb()


@pytest.fixture
def fastapi_app():
    from api.main import app
    return app


@pytest.fixture
def client(fastapi_app):
    return TestClient(fastapi_app)


@pytest.fixture
def app(client):
    from client import App
    return App(client=client)


@pytest.fixture
def user_service(conn):
    from api.services.user import UserService
    return UserService(conn)


@pytest.fixture
def organization_service(conn):
    from api.services.organization import OrganizationService
    return OrganizationService(conn)


@pytest.fixture
def vacancy_service(conn, organization_service):
    from api.services.vacancy import VacancyService
    return VacancyService(conn, organization_service)


@pytest.fixture
def user_db(user_service):
    user_create = UserCreate(
        name="test user"
    )
    user_db = user_service.create_user(user_create)
    return user_db


@pytest.fixture
def organization_db(organization_service):
    organization_create = OrganizationCreate(
        name="test org"
    )
    organization_db = organization_service.create_organization(organization_create)
    return organization_db


@pytest.fixture
def vacancy_create(organization_db):
    vacancy_create = VacancyCreate(
        title="test vacancy",
        organization_id=organization_db.public_id,
    )
    return vacancy_create


@pytest.fixture
def vacancy_db(vacancy_create, vacancy_service):
    vacancy_db = vacancy_service.create_vacancy(vacancy_create)
    return vacancy_db