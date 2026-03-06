from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    ForeignKey,
    Text
)


metadata = MetaData()


user = Table(
    "user", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
)

organization = Table(
    "organization", metadata,
    Column("name", String, primary_key=True)
)

vacancy = Table(
    "vacancy", metadata,
    Column("id", Integer, primary_key=True),
    Column("organization", ForeignKey("organization.name")),
    Column("title", String),
)

application = Table(
    "application", metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("vacancy_id", ForeignKey("user.id"), primary_key=True),
)

message = Table(
    "messages", metadata,
    Column("id", Integer, primary_key=True),
    Column("recipient_id", ForeignKey("user.id"), nullable=False),
    Column("text", Text)
)