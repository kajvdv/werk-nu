import pytest
from fastapi.testclient import TestClient


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


@pytest.fixture(name="user_controller")
def user_controller_fixture(conn):
    from api.dependencies.user import UserController
    return UserController(conn)


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