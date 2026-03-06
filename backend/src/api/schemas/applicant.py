from pydantic import BaseModel

from .user import UserPublic, UserDB
from .vacancy import VacancyPublic, VacancyDB

class ApplicantBase(BaseModel):
    ...


class ApplicantPublic(ApplicantBase):
    user: UserPublic
    vacancy: VacancyPublic


class ApplicationCreate(ApplicantBase):
    # vacancy: VacancyPublic
    ...
    

class ApplicationDB(ApplicantBase):
    user: UserDB
    vacancy: VacancyDB