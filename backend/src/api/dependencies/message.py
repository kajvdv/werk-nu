from fastapi import Depends
from sqlalchemy import insert, select, Connection

from api.database import get_conn
from api.schemas.message import MessageCreate, MessageDB
from api.tables import message


class MessageController:
    def __init__(
            self,
            conn: Connection = Depends(get_conn)
    ) -> None:
        self.conn = conn

    def add_message(self, recipient_id, message_data: MessageCreate):
        stmt = (
            insert(message)
            .values(
                recipient_id=recipient_id,
                **message_data.model_dump()
            )
            .returning(message)
        )
        row = self.conn.execute(stmt).first()
        self.conn.commit()
        if not row:
            raise Exception("Failed to insert message")
        return MessageDB.model_validate(row, from_attributes=True)