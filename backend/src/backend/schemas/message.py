from pydantic import BaseModel


class MessageBase(BaseModel):
    text: str


class MessageCreate(MessageBase):
    ...


class MessagePublic(MessageBase):
    ...


class MessageDB(MessageBase):
    ...