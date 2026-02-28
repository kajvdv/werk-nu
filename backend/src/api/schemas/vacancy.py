from pydantic import BaseModel, field_validator


class VacancyBase(BaseModel):
    title: str
    organization: str


class VacancyCreate(VacancyBase):
    ...


class VacancyPublic(VacancyBase):
    id: str

    @field_validator("id", mode="before")
    @classmethod
    def obfuscate_id(cls, value): #TODO: encrypt id somehow
        return str(value)


class VacancyDB(VacancyBase):
    id: int