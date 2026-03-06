from uuid import UUID

from pydantic import BaseModel, Field


class VacancyBase(BaseModel):
    title: str


class VacancyCreate(VacancyBase):
    organization_id: UUID


class VacancyPublic(VacancyBase):
    organization_id: UUID
    id: UUID = Field(validation_alias="public_id")


class VacancyDB(VacancyBase):
    id: int
    public_id: UUID
    organization_id: int