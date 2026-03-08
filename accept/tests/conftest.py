import pytest
from dotenv import load_dotenv
import httpx


pytest.register_assert_rewrite("client")


@pytest.fixture(autouse=True)
def load_env_vars():
    load_dotenv(".env")


@pytest.fixture(name="conn", autouse=True)
def connection(load_env_vars):
    from api.database import engine, get_conn
    from api.tables import metadata
    metadata.create_all(engine)
    for conn in get_conn():
        yield conn
    metadata.drop_all(engine)


@pytest.fixture
def app():
    from client import App
    return App(httpx.Client(base_url="http://localhost:8000/"))


@pytest.fixture
def auth_service(conn):
    from api.services.auth import AuthService
    return AuthService(conn)


@pytest.fixture
def user_service(conn, auth_service):
    from api.services.user import UserService
    return UserService(conn, auth_service)


@pytest.fixture
def organization_service(conn, auth_service):
    from api.services.organization import OrganizationService
    return OrganizationService(conn, auth_service)


@pytest.fixture
def vacancy_service(conn, organization_service):
    from api.services.vacancy import VacancyService
    return VacancyService(conn, organization_service)
