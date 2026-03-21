import uuid

from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()


user = Table(
    "user", metadata,
    Column("id", ForeignKey("auth_user.id"), primary_key=True),
    Column("name", String, nullable=False),
)

auth_user = Table(
    "auth_user", metadata,
    Column("id", Integer, primary_key=True),
    Column("public_id", UUID(as_uuid=True), default=uuid.uuid4, nullable=False),
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("entity_type", String, nullable=False),
    Column("active", Boolean, nullable=False, default=False)
)

activation_link = Table(
    "activation_link", metadata,
    Column("code", String, nullable=False),
    Column("user_id", ForeignKey("auth_user.id"))
)

organization = Table(
    "organization", metadata,
    Column("id", ForeignKey("auth_user.id"), primary_key=True),
    Column("name", String, unique=True, nullable=False)
)

vacancy = Table(
    "vacancy", metadata,
    Column("id", Integer, primary_key=True),
    Column("public_id", UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
    Column("organization_id", ForeignKey("organization.id"), nullable=False),
    Column("title", String, nullable=False),
)

application = Table(
    "application", metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("vacancy_id", ForeignKey("vacancy.id"), primary_key=True),
)

message = Table(
    "messages", metadata,
    Column("id", Integer, primary_key=True),
    Column("recipient_id", ForeignKey("user.id"), nullable=False),
    Column("text", Text)
)