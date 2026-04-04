import os

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from backend.schemas.vacancy import VacancyCreate, VacancyPublic
from backend.schemas.applicant import ApplicantPublic
from backend.schemas.user import UserCreate
from backend.schemas.organization import OrganizationCreate
from backend.schemas.message import MessageCreate, MessagePublic

from .brower import connect

FRONTEND_URL = os.environ["FRONTEND_URL"]

class SeleniumDriver:
    def __init__(self, port: int) -> None:
        self.driver = connect(port)
        self.driver.get(FRONTEND_URL)

    def _find_element_by_id(self, id):
        return self.driver.find_element(value=id)
    
    def register_organization(self, organization_data: OrganizationCreate):
        self.driver.get(f"{FRONTEND_URL}")
        element = self.driver.find_element(By.ID, "register-organization")
        element.click()
        assert self.driver.current_url.endswith("/organizations/register")
        
        # Fill in registration form
        element = self._find_element_by_id("org-name")
        element.send_keys(organization_data.name)

        element = self._find_element_by_id("org-email")
        element.send_keys(organization_data.email)

        element = self._find_element_by_id("org-password")
        element.send_keys(organization_data.password)

        element = self._find_element_by_id("register-org-submit")
        element.click()

        element = self._find_element_by_id("successful-register")
        
    def register_user(self, user_data: UserCreate):
        self.driver.get(f"{FRONTEND_URL}")
        element = self.driver.find_element(By.ID, "register-user")
        element.click()
        assert self.driver.current_url.endswith("/users/register")

        # Fill in registration form
        element = self._find_element_by_id("user-name")
        element.send_keys(user_data.name)

        element = self._find_element_by_id("user-email")
        element.send_keys(user_data.email)

        element = self._find_element_by_id("user-password")
        element.send_keys(user_data.password)

        element = self._find_element_by_id("register-user-submit")
        element.click()

        element = self._find_element_by_id("successful-register")

        
    def activate_account(self, code):
        self.driver.get(f"{FRONTEND_URL}/api/register/activate/{code}")
        

    def login(self, email: str, password: str):
        self.driver.get(f"{FRONTEND_URL}/login")

        element = self._find_element_by_id("login-username")
        element.send_keys(email)

        element = self._find_element_by_id("login-password")
        element.send_keys(password)

        element = self._find_element_by_id("login-submit")
        element.click()
        
        
    def post_vacancy(self, vacancy: VacancyCreate) -> VacancyPublic:
        self.driver.get(f"{FRONTEND_URL}/organizations/me")
        element = self._find_element_by_id("post-vacancy")
        element.click()

        element = self._find_element_by_id("post-vacancy-title")
        element.send_keys(vacancy.title)

        element = self._find_element_by_id("post-vacancy-submit")
        element.click()

        element = self._find_element_by_id("confirm-post")
        element.click()

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        element = soup.find(id="submitted-vacancy")

        # Parse VacancyPublic
        divs = element.find_all('div')

        return VacancyPublic.model_validate({
            "title": divs[0].text,
            "organization_id": divs[1].text,
            "id": divs[2].text,
        }, by_name=True)

        
    def post_application(self, vacancy: VacancyPublic):
        self.driver.get(f"{FRONTEND_URL}/vacancies")

        element = self.driver.find_element(value=f"{vacancy.id}-apply")
        element.click()

        
    def get_applicants(self, vacancy: VacancyPublic) -> list[ApplicantPublic]:
        self.driver.get(f"{FRONTEND_URL}/vacancies/me")

        # element = self.driver.find_element(value=f"{vacancy.id}")
        # elements = self.driver.find_elements(By.CLASS_NAME, "application")
        
    def get_messages(self) -> list[MessagePublic]:
        raise NotImplementedError()
        
    def send_message(self, user_id, message: MessageCreate):
        raise NotImplementedError()
        