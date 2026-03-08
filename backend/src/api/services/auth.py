from sqlalchemy import Connection, select, insert

from api.schemas.auth import AuthCreate, AuthDB
from api.schemas.token import TokenCreate
from api.tables import auth_user
from auth.auth import authenticate_user, hash_password, create_access_token, decode_token


class AuthService:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def create_auth_user(self, auth_create: AuthCreate):
        hashed_password = hash_password(auth_create.password)
        row = self.conn.execute(
            insert(auth_user)
            .values({
                "hashed_password": hashed_password,
                **auth_create.model_dump(include={
                    "email", "entity_type"
                })
            })
            .returning(auth_user)
        ).first()
        return AuthDB.model_validate(row, from_attributes=True)

    def get_auth_user(self, email: str):
        row = self.conn.execute(
            select(auth_user)
            .where(auth_user.c.email == email)
            .limit(1)
        ).first()
        return AuthDB.model_validate(row, from_attributes=True)
        
    def login(self, email, password):
        hashed_password = self.conn.scalar(
            select(auth_user.c.hashed_password)
            .where(auth_user.c.email == email)
            .limit(1)
        )
        if not hashed_password or not authenticate_user(password, hashed_password):
            return False
        else:
            return True
        
    def create_access_token(self, token_create: TokenCreate):
        return create_access_token(token_create.model_dump())

    def decode_token(self, token):
        return decode_token(token)