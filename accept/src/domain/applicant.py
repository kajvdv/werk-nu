from __future__ import annotations
from typing import TYPE_CHECKING

from domain.users import User
from domain.application import Application

from api.schemas.user import UserCreate

if TYPE_CHECKING:
    from domain.vacancy import Vacancy


class Applicant(User):

    def __init__(self, email: str) -> None:
        super().__init__()
        self.app.register_user(UserCreate(
            name="Test user",
            email=email,
            password="password",
        ))
        self.app.login(email, "password")    
    
    def apply(self, vacancy: Vacancy) -> Application:
        public_schema = self.app.post_application(vacancy.vacancy)
        return Application(
            public_schema,
            vacancy.employer_client,
            user_client=self.app,
        )