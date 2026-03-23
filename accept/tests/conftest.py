import pytest
from dotenv import load_dotenv
import httpx

pytest.register_assert_rewrite("accept")

from storyteller import StoryTeller


@pytest.fixture(autouse=True, scope="class")
def load_env_vars():
    load_dotenv(".env")


@pytest.fixture(autouse=True)
def reset_db():
    from backend.cli import resetdb
    resetdb()


@pytest.fixture(params=[
    "http",
    # "selenium",
], scope="class")
def driver_factory(request, load_env_vars):
    from driver_factory import HttpDriverFactory, SeleniumDriverFactory
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
