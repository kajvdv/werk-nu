from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

from backend.schemas.vacancy import VacancyPublic
from backend.schemas.user import UserCreate
from backend.schemas.applicant import ApplicantPublic
from accept.drivers import Driver
from accept.domain.user import User


class Applicant(User):
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

    def register(self):
        self.driver.register_user(UserCreate(
            name=self.name,
            email=self.email,
            password=self.password,
        ))

    def apply(self, vacancy: VacancyPublic) -> ApplicantPublic:
        return self.driver.post_application(vacancy)
