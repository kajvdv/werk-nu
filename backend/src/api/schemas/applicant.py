from pydantic import BaseModel

from .user import UserPublic
from .vacancy import VacancyPublic

class ApplicantBase(BaseModel):
    ...


class ApplicantPublic(ApplicantBase):
    user: UserPublic
    vacancy: VacancyPublic


class ApplicationCreate(BaseModel):
    # vacancy: VacancyPublic
    ...
    