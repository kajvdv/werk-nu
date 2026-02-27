from pydantic import BaseModel


class VacancyCreate(BaseModel):
    title: str