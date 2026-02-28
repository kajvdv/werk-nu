from pydantic import BaseModel, field_validator


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    ...


class UserPublic(UserBase):
    id: str

    @field_validator("id", mode="before")
    @classmethod
    def obfuscate_id(cls, value): #TODO: encrypt id somehow
        return str(value)


class UserDB(UserBase):
    id: int