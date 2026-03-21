from uuid import UUID

from sqlalchemy import Connection, select, insert

from backend.schemas.organization import OrganizationCreate, OrganizationDB
from backend.schemas.auth import AuthCreate
from backend.services.auth import AuthService
from backend.queries.organization import select_organization
from backend.tables import organization


class OrganizationService:
    def __init__(self,
            conn: Connection,
            auth_service: AuthService,
    ) -> None:
        self.conn = conn
        self.auth_service = auth_service

    def create_organization(self, data: OrganizationCreate):
        auth_user = self.auth_service.create_auth_user(AuthCreate(
            email=data.email,
            password=data.password,
            entity_type="organization",
        ))
        row = self.conn.execute(
            insert(organization)
            .values({
                "id": auth_user.id,
                **data.model_dump(exclude={
                    "email", "password"
                })
            })
            .returning(organization)
        ).first()
        return OrganizationDB.model_validate({**row._mapping, **auth_user.model_dump()})
    
    def get_organization(self, *,
            id: int | None = None,
            public_id: UUID | None = None
    ):
        row = self.conn.execute(select_organization(
            id=id,
            public_id=public_id,
        )).first()
        if not row:
            raise Exception(f"No organization found.")
        return OrganizationDB.model_validate(row, from_attributes=True)