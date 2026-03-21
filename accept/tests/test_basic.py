import pytest

from backend.schemas.vacancy import VacancyCreate
from backend.schemas.message import MessageCreate

from accept.domain.employer import Employer
from accept.domain.applicant import Applicant


class TestApplying:
    @pytest.fixture
    def vacancy_data(self):
        return VacancyCreate(
            title="test vacancy",
        )
    
    @pytest.fixture(autouse=True)
    def auth_john_doe(self, john_doe: Applicant):
        john_doe.register()
        john_doe.activate_account()
        john_doe.login()

    @pytest.fixture(autouse=True)
    def auth_acme_corp(self, acme_corp: Employer):
        acme_corp.register()
        acme_corp.activate_account()
        acme_corp.login()

    
    def test_applicant_can_apply_to_vacancy_posted_by_employer(self,
            vacancy_data: VacancyCreate,
            acme_corp: Employer,
            john_doe: Applicant,
    ):
        vacancy = acme_corp.create_vacancy(vacancy_data)
        john_doe.apply(vacancy)

        acme_corp.assert_applicant_applied_to_vacancy(john_doe, vacancy)


    def test_employer_can_reach_out_to_applicant_after_reviewing_application(self,
            vacancy_data: VacancyCreate,
            acme_corp: Employer,
            john_doe: Applicant,
    ):
        vacancy = acme_corp.create_vacancy(vacancy_data)
        john_doe.apply(vacancy)
        applicants = acme_corp.get_applicants(vacancy)
        acme_corp.send_message(
            to=str(applicants[0].user.id),
            message=MessageCreate(text="Hello applicant")
        )

        assert "Hello applicant" in john_doe.messages
    
    # def test_get_overview_of_applied_vacancies(self):
    #     """User gets all the vacancies they applied to"""