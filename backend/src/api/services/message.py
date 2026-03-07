from sqlalchemy import Connection, insert, select

from api.schemas.message import MessageCreate, MessageDB
from api.schemas.user import UserDB
from api.tables import message


class MessageService:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def create_message(self, recipient: UserDB, data: MessageCreate) -> MessageDB:
        stmt = (
            insert(message)
            .values(
                recipient_id=recipient.id,
                **data.model_dump()
            )
            .returning(message)
        )
        row = self.conn.execute(stmt).first()
        self.conn.commit()
        return MessageDB.model_validate(row, from_attributes=True)
    
    def get_messages(self, user_db: UserDB):
        stmt = (
            select(message)
            .where(message.c.recipient_id == user_db.id)
        )
        messages = self.conn.execute(stmt)
        return [MessageDB.model_validate(m, from_attributes=True) for m in messages]