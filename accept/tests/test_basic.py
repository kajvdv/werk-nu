import pytest

from api.schemas.vacancy import VacancyCreate

from domain.employer import Employer
from domain.applicant import Applicant


class TestApplying:

    @pytest.fixture
    def organization(self, organization_service):
        from api.schemas.organization import OrganizationCreate
        organization = organization_service.create_organization(OrganizationCreate(
            name="test employer",
            email="test@org.com",
            password="password",
        ))
        organization_service.conn.commit()
        return organization
    
    @pytest.fixture
    def vacancy_data(self):
        return VacancyCreate(
            title="test vacancy",
        )

    @pytest.fixture
    def employer(self):
        return Employer(
            name="Acme Corp",
            email="test@org.com"
        )

    @pytest.fixture
    def applicant(self):
        return Applicant("test@test.com")
    
    def test_applicant_can_apply_to_vacancy_posted_by_employer(self,
            vacancy_data: VacancyCreate,
            employer: Employer,
            applicant: Applicant,
    ):
        vacancy = employer.create_vacancy(vacancy_data)
        application = applicant.apply(vacancy)

        assert application.in_vacancy(vacancy)

    def test_employer_can_reach_out_to_applicant_after_reviewing_application(self,
            vacancy_data: VacancyCreate,
            employer: Employer,
            applicant: Applicant,
    ):
        vacancy = employer.create_vacancy(vacancy_data)
        application = applicant.apply(vacancy)
        application.send_message(
            text="Hello applicant"
        )

        assert "Hello applicant" in applicant.messages
    
    def test_get_overview_of_applied_vacancies(self):
        """User gets all the vacancies they applied to"""