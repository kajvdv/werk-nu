from pydantic import BaseModel, EmailStr, UUID4, field_serializer


class TokenBase(BaseModel):
    sub: str
    email: EmailStr
    name: str
    id: UUID4
    entity_type: str

    @field_serializer("id", "plain", check_fields=False)
    def serialize_uuid(self, value: UUID4):
        return str(value)


class TokenCreate(TokenBase):
    sub: str
