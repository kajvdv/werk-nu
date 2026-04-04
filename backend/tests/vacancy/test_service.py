import pytest

from backend.schemas.vacancy import VacancyCreate


@pytest.fixture(scope="class")
def vacancy_service(conn, organization_service, uuid_factory):
    from backend.services.vacancy import VacancyService
    return VacancyService(conn, organization_service, uuid_factory)


class TestCRUDVacancy:
    @pytest.fixture
    def data(self):
        return VacancyCreate(
            title="Test vacancy",
            organization="test organization",
            location="Somewhere",
            availability="Fulltime"
        )

    def test_return_public_vacancy(self, vacancy_service, organization_db, data):
        vacancy_public = vacancy_service.create_vacancy(data, organization_db.public_id)