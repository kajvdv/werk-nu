from uuid import UUID

from sqlalchemy import Connection, select, insert

from api.schemas.user import UserCreate, UserDB
from api.tables import user


class UserService:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def create_user(self, data: UserCreate):
        row = self.conn.execute(
            insert(user)
            .values(
                **data.model_dump()
            )
            .returning(user)
        ).first()
        self.conn.commit()
        return UserDB.model_validate(row, from_attributes=True)

    def get_user(self, public_id: UUID):
        row = self.conn.execute(
            select(user)
            .where(user.c.public_id == public_id)
        ).first()
        if not row:
            raise Exception(f"No user with id {public_id}")
        return UserDB.model_validate(row, from_attributes=True)