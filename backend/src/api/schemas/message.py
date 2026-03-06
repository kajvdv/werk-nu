from pydantic import BaseModel


class MessageBase(BaseModel):
    text: str


class MessageCreate(MessageBase):
    recipient_id: int


class MessagePublic(MessageBase):
    ...


class MessageDB(MessageBase):
    ...