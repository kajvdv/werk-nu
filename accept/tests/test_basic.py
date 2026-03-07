import pytest

from api.schemas.vacancy import VacancyCreate

from domain.employer import Employer
from domain.applicant import Applicant


@pytest.fixture(name="message_controller")
def message_controller_fixture(conn):
    from api.dependencies.message import MessageController
    controller = MessageController(conn)
    return controller


class TestApplying:
    @pytest.fixture
    def organization(self, conn):
        from api.services.organization import OrganizationService
        from api.schemas.organization import OrganizationCreate
        controller = OrganizationService(conn)
        return controller.create_organization(OrganizationCreate(
            name="test employer"
        ))
    
    @pytest.fixture
    def vacancy_data(self, organization):
        return VacancyCreate(
            title="test vacancy",
            organization_id=organization.public_id
        )

    @pytest.fixture(autouse=True)
    def add_applicant(self, conn):
        from api.services.user import UserService
        from api.schemas.user import UserCreate
        user_service = UserService(conn)
        user_service.create_user(UserCreate(
            name="test user"
        ))
    
    def test_applicant_can_apply_to_vacancy_posted_by_employer(self, vacancy_data):
        employer = Employer.from_name("Acme Corp")
        applicant = Applicant.from_id("1")

        vacancy = employer.post_vacancy(vacancy_data)
        application = applicant.apply(vacancy)

        assert application == vacancy.received_applications()[0]


    def test_employer_can_reach_out_to_applicant_after_reviewing_application(self, vacancy_data):
        employer = Employer.from_name("Acme Corp")
        applicant = Applicant.from_id("1")

        vacancy = employer.post_vacancy(vacancy_data)
        application = applicant.apply(vacancy)
        application.send_message(
            text="We'd love to schedule an interview!"
        )

        assert "We'd love to schedule an interview!" in applicant.messages

    
    def test_get_overview_of_applied_vacancies(self):
        """User gets all the vacancies they applied to"""