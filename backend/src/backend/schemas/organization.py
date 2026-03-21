from pydantic import BaseModel, UUID4, Field, EmailStr


class OrganizationBase(BaseModel):
    name: str
    email: EmailStr


class OrganizationCreate(OrganizationBase):
    password: str


class OrganizationPublic(OrganizationBase):
    id: UUID4 = Field(validation_alias="public_id")


class OrganizationDB(OrganizationBase):
    id: int
    public_id: UUID4