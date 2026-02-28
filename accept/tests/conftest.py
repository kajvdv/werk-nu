import pytest
from dotenv import load_dotenv


pytest.register_assert_rewrite("client")


@pytest.fixture(autouse=True)
def load_env_vars():
    load_dotenv(".env")


@pytest.fixture(name="conn")
def connection():
    from api.database import engine, get_conn
    from api.tables import metadata
    metadata.create_all(engine)
    for conn in get_conn():
        yield conn
    metadata.drop_all(engine)




@pytest.fixture
def app():
    from client import App
    return App()