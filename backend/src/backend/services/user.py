from uuid import UUID

from sqlalchemy import Connection, select, insert

from backend.services.auth import AuthService
from backend.services.message import MessageService
from backend.schemas.user import UserCreate, UserDB
from backend.schemas.auth import AuthCreate
from backend.queries.user import select_user
from backend.tables import user


class UserService:
    def __init__(self,
            conn: Connection,
            auth_service: AuthService,
    ) -> None:
        self.conn = conn
        self.auth_service = auth_service

    def create_user(self, data: UserCreate):
        auth_user = self.auth_service.create_auth_user(AuthCreate(
            email=data.email,
            password=data.password,
            entity_type="user",
        ))
        row = self.conn.execute(
            insert(user)
            .values({
                "id": auth_user.id,
                **data.model_dump(exclude={
                    "email",
                    "password",
                })
            })
            .returning(user)
        ).first()
        return UserDB.model_validate({**row._mapping, **auth_user.model_dump()})

    def get_user(self, *,
            id: int | None = None,
            public_id: UUID | None = None
    ):
        row = self.conn.execute(select_user(
            id=id,
            public_id=public_id,
        )).first()
        if not row:
            raise Exception(f"No user found")
        
        return UserDB.model_validate(row, from_attributes=True)
