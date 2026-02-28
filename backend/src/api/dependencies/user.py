from fastapi import Depends
from sqlalchemy import insert, select, Connection

from api.schemas.user import UserCreate, UserDB
from api.tables import user
from api.database import get_conn


def get_user(
        conn: Connection = Depends(get_conn)
):
    stmt = (
        select(user)
        .where(user.c.id == 1)
    )
    row = conn.execute(stmt).first()
    return UserDB.model_validate(row, from_attributes=True)


class UserController:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn 
    
    def add_user(self, user_data: UserCreate):
        stmt = (
            insert(user)
            .values(**user_data.model_dump())
            .returning(user)
        )
        row = self.conn.execute(stmt).first()
        if not row:
            raise Exception("Failed to insert user")
        self.conn.commit()
        return UserDB.model_validate(row, from_attributes=True)