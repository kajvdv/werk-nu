from datetime import datetime

from pydantic import BaseModel, Field, field_serializer, UUID4


class VacancyBase(BaseModel):
    title: str
    organization: str
    location: str
    availability: str


class VacancyCreate(VacancyBase):
    ...


class VacancyPublic(VacancyBase):
    organization_id: UUID4
    id: UUID4 = Field(validation_alias="public_id")
    newVacancy: bool = False
    closed: bool = False
    
    @field_serializer("organization_id", "id", mode="plain", check_fields=False)
    def serialize_uuid(self, value: UUID4):
        return str(value)


class VacancyPublicOwn(VacancyPublic):
    created_at: datetime
    applyCount: int


class VacancyDB(VacancyBase):
    created_at: datetime
    id: int
    public_id: UUID4
    organization_id: int