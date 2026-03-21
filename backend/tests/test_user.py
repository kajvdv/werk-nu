from typing import TYPE_CHECKING

import pytest

from backend.schemas.user import UserPublic


def test_primary_key_not_public(user_service, user_create):
    model = user_service.create_user(user_create)
    public_schema = UserPublic.model_validate(model, from_attributes=True)
    assert public_schema.id != "1"
