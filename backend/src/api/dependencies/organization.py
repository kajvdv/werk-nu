from sqlalchemy import select, insert, Connection

from api.schemas.organization import OrganizationCreate, OrganizationDB
from api.tables import organization


class OrganizationController:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
    
    def add_organization(self, organization_data: OrganizationCreate) -> OrganizationDB:
        stmt = (
            insert(organization)
            .values(**organization_data.model_dump())
            .returning(organization)
        )
        row = self.conn.execute(stmt).first()
        if not row:
            raise Exception("Failed to insert organization")
        self.conn.commit()
        return OrganizationDB.model_validate(row, from_attributes=True)
