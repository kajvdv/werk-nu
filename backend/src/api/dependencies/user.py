from fastapi import Depends
from sqlalchemy import insert, select, Connection
import nanoid

from api.schemas.user import UserCreate, UserDB
from api.schemas.message import MessageDB
from api.tables import user, message
from api.database import get_conn


class UserController:
    def __init__(
            self,
            conn: Connection = Depends(get_conn)
        ) -> None:
        self.conn = conn 
    
    def add_user(self, user_data: UserCreate):
        public_id = nanoid.generate(size=12)
        stmt = (
            insert(user)
            .values(
                public_id=public_id,
                **user_data.model_dump()
            )
            .returning(user)
        )
        row = self.conn.execute(stmt).first()
        if not row:
            raise Exception("Failed to insert user")
        self.conn.commit()
        return UserDB.model_validate(row, from_attributes=True)

    def get_user(self):
        stmt = (
            select(user)
            .where(user.c.id == 1)
        )
        row = self.conn.execute(stmt).first()
        return UserDB.model_validate(row, from_attributes=True)

    def get_messages(self):
        user = self.get_user()
        stmt = (
            select(message)
            .where(message.c.recipient_id == user.id)
        )
        messages = self.conn.execute(stmt)
        return (MessageDB.model_validate(m, from_attributes=True) for m in messages)