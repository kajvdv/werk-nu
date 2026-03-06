from sqlalchemy import Connection, select, insert

from api.schemas.user import UserCreate, UserDB, UserPublic
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

    def get_user(self, data: UserPublic):
        row = self.conn.execute(
            select(user)
            .where(user.c.public_id == data.id)
        ).first()
        return UserDB.model_validate(row, from_attributes=True)