import pytest

from api.schemas.vacancy import VacancyCreate

from domain.users import Employer, Applicant



class TestApplying:
    @pytest.fixture
    def vacancy_data(self):
        return VacancyCreate(
            title="test vacancy",
            organization="test employer"
        )
    
    @pytest.fixture(autouse=True)
    def add_employer(self, conn):
        from api.dependencies.organization import OrganizationController
        from api.schemas.organization import OrganizationCreate
        controller = OrganizationController(conn)
        controller.add_organization(OrganizationCreate(
            name="test employer"
        ))

    @pytest.fixture(autouse=True)
    def add_applicant(self, conn):
        from api.dependencies.user import UserController
        from api.schemas.user import UserCreate
        controller = UserController(conn)
        controller.add_user(UserCreate(
            name="test user"
        ))
    
    def test_applicant_can_apply_to_vacancy_posted_by_employer(self, app, vacancy_data):
        employer = Employer(app)
        applicant = Applicant(app)

        vacancy = employer.post_vacancy(vacancy_data)
        application = applicant.apply(vacancy)

        assert application == vacancy.received_applications()[0]


    def test_employer_can_reach_out_to_applicant_after_reviewing_application(self, app, vacancy_data):
        employer = Employer(app)
        applicant = Applicant(app)

        vacancy = employer.post_vacancy(vacancy_data)
        application = applicant.apply(vacancy)
        application.send_message(
            text="We'd love to schedule an interview!"
        )

        assert "We'd love to schedule an interview!" in applicant.messages