import pytest


@pytest.fixture
def app():
    from domain.app import App
    return App()