from pydantic import BaseModel, Field, UUID4


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    ...


class UserPublic(UserBase):
    id: UUID4 = Field(validation_alias="public_id")


class UserDB(UserBase):
    id: int
    public_id: UUID4