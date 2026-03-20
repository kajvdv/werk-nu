from pydantic import BaseModel, EmailStr, UUID4, Field


class AuthBase(BaseModel):
    email: EmailStr
    entity_type: str
    active: bool = Field(default=False)


class AuthCreate(AuthBase):
    password: str


class AuthPublic(AuthBase):
    name: str


class AuthDB(AuthBase):
    id: int
    public_id: UUID4
    hashed_password: str