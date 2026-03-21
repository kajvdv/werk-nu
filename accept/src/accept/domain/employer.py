from __future__ import annotations
from typing import TYPE_CHECKING

from backend.schemas.vacancy import VacancyCreate, VacancyPublic
from backend.schemas.organization import OrganizationCreate
from accept.domain.user import User
from accept.drivers import Driver

if TYPE_CHECKING:
    from accept.domain.applicant import Applicant


class Employer(User):
    def __init__(self,
            driver: Driver,
            name: str,
            email: str,
            password: str,
    ) -> None:
        super().__init__(driver)
        self.name = name
        self.email = email
        self.password = password

    def register(self) -> None:
        self.driver.register_organization(OrganizationCreate(
            name=self.name,
            email=self.email,
            password=self.password,
        ))
        
    def create_vacancy(self, vacancy: VacancyCreate) -> VacancyPublic:
        return self.driver.post_vacancy(vacancy)

    def get_applicants(self, vacancy: VacancyPublic):
        return self.driver.get_applicants(vacancy)
    
    def assert_applicant_applied_to_vacancy(self,
            applicant: Applicant,
            vacancy: VacancyPublic
    ) -> None:
        applicants = self.driver.get_applicants(vacancy)
        assert applicant.email in [a.user.email for a in applicants]
    