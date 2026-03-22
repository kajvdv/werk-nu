import pytest
from dotenv import load_dotenv
import httpx

pytest.register_assert_rewrite("accept")

from accept.drivers import Driver
from accept.drivers.http import HttpDriver
from accept.drivers.selenium import SeleniumDriver
from storyteller import StoryTeller


class HttpDriverFactory:
    def create_driver(self) -> Driver:
        return HttpDriver()

class SeleniumDriverFactory:
    def __init__(self) -> None:
        self.i = 0
    
    def _get_next_port(self) -> int:
        ports = [9222, 9223] # Stupid, I know
        port = ports[self.i]
        self.i += 1
        return port
    
    def create_driver(self) -> Driver:
        return SeleniumDriver(self._get_next_port())


@pytest.fixture(autouse=True, scope="class")
def load_env_vars():
    load_dotenv(".env")


@pytest.fixture(autouse=True)
def reset_db():
    from backend.cli import resetdb
    resetdb()


@pytest.fixture(params=[
    # "http",
    "selenium",
], scope="class")
def driver_factory(request, load_env_vars):
    driver_name = request.param
    match driver_name:
        case "http":
            return HttpDriverFactory()
        case "selenium":
            return SeleniumDriverFactory()
        case _:
            raise Exception(f"No driver for {driver_name}")


@pytest.fixture
def story_teller(driver_factory):
    return StoryTeller(driver_factory)


@pytest.fixture
def acme_corp(story_teller):
    return story_teller.spawn_employer(
        name="Acme Corp",
        email="info@acmecorp.com",
        password="password"
    )


@pytest.fixture
def john_doe(story_teller):
    return story_teller.spawn_applicant(
        name="John Doe",
        email="johndoe@mail.com",
        password="password"
    )
