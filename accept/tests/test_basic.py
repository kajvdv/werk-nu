import pytest

from api.schemas import VacancyCreate

from domain.users import Employer, Applicant



class TestApplying:
    @pytest.fixture
    def vacancy_data(self):
        return VacancyCreate(
            title="test vacancy"
        )
    
    def test_applicant_can_apply_to_vacancy_posted_by_employer(self, app, vacancy_data):
        employer = Employer(app)
        applicant = Applicant(app)

        vacancy = employer.post_vacancy(vacancy_data)
        applicant.apply(vacancy)

        assert applicant == vacancy.received_applications()[0]


    def test_employer_can_reach_out_to_applicant_after_reviewing_application(self, app, vacancy_data):
        employer = Employer(app)
        applicant = Applicant(app)

        vacancy = employer.post_vacancy(vacancy_data)
        application = applicant.apply(vacancy)
        application.send_message(
            text="We'd love to schedule an interview!"
        )

        assert "We'd love to schedule an interview!" in applicant.messages