from pydantic import BaseModel, Field, field_serializer, UUID4


class VacancyBase(BaseModel):
    title: str


class VacancyCreate(VacancyBase):
    ...


class VacancyPublic(VacancyBase):
    organization_id: UUID4
    id: UUID4 = Field(validation_alias="public_id")
    
    @field_serializer("organization_id", "id", mode="plain", check_fields=False)
    def serialize_uuid(self, value: UUID4):
        return str(value)


class VacancyDB(VacancyBase):
    id: int
    public_id: UUID4
    organization_id: int