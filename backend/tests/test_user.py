from typing import TYPE_CHECKING

import pytest

from api.schemas.user import UserPublic, UserCreate


def test_primary_key_not_public(user_service):
    model = user_service.create_user(UserCreate(
        name="test user"
    ))
    public_schema = UserPublic.model_validate(model, from_attributes=True)
    assert public_schema.id != "1"
