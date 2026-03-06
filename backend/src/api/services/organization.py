from sqlalchemy import Connection, select, insert

from api.schemas.organization import OrganizationCreate, OrganizationDB
from api.tables import organization


class OrganizationService:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def create_organization(self, data: OrganizationCreate):
        row = self.conn.execute(
            insert(organization)
            .values(
                **data.model_dump()
            )
            .returning(organization)
        ).first()
        self.conn.commit()
        return OrganizationDB.model_validate(row, from_attributes=True)