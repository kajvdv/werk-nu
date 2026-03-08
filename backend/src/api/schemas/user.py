from pydantic import BaseModel, Field, UUID4, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: UUID4 = Field(validation_alias="public_id")


class UserDB(UserBase):
    id: int
    public_id: UUID4