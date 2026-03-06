from uuid import UUID

from pydantic import BaseModel


class OrganizationBase(BaseModel):
    name: str


class OrganizationCreate(OrganizationBase):
    ...


class OrganizationDB(OrganizationBase):
    id: int
    public_id: UUID