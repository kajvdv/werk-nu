import pytest

from api.schemas.token import TokenCreate
from api.schemas.user import UserDB


class TestAuthUser:
    @pytest.fixture
    def token_create(self, user_db: UserDB):
        return TokenCreate(
            sub=user_db.name,
            email=user_db.email,
            name=user_db.name,
            id=user_db.public_id,
            entity_type="user"
        )
    
    def test_user_can_login(self, user_db, auth_service):
        success = auth_service.login(user_db.email, "password")
        assert success

    def test_access_token_data_contains_entity_type(self, user_db, auth_service, token_create):
        auth_service.login(user_db.email, "password")
        token = auth_service.create_access_token(token_create)
        assert "entity_type" in auth_service.decode_token(token)


class TestAuthOrg:

    def test_only_org_can_get_its_applications(self):
        ...