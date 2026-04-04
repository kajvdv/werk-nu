import pytest

from backend.repository import Model, Repository


class FakeModel(Model):
    def update(self, model: Model) -> None: ... 


class FakeRepository(Repository):
    def get(self, id) -> Model: ...
    def delete(self, model: Model) -> None: ...


@pytest.fixture
def repository():
    return FakeRepository()


class TestRepositry:
    def test_create_fake_model(self, data):
        model = FakeModel(**data)
