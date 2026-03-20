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
        pw = "password"
        self.app.register_user(UserCreate(
            name="Test user",
            email=email,
            password=pw,
        ))
        self._activate_account()
        self.app.login(email, pw)    
    
    def apply(self, vacancy: Vacancy) -> Application:
        public_schema = self.app.post_application(vacancy.vacancy)
        return Application(
            public_schema,
            vacancy.employer_client,
            user_client=self.app,
        )