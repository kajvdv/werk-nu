from uuid import UUID

from sqlalchemy import Connection, select, insert

from api.services.auth import AuthService
from api.services.message import MessageService
from api.schemas.user import UserCreate, UserDB
from api.schemas.auth import AuthCreate
from api.queries.user import select_user
from api.tables import user


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
