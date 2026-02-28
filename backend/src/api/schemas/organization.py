from pydantic import BaseModel


class OrganizationBase(BaseModel):
    name: str


class OrganizationCreate(OrganizationBase):
    ...


class OrganizationDB(OrganizationBase):
    # id: int
    ...