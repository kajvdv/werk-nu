import os
import uuid
from secrets import token_urlsafe
from typing import Callable
from uuid import UUID

from sqlalchemy import Connection, select, insert, delete, update

from backend.schemas.auth import AuthCreate, AuthDB
from backend.schemas.token import TokenCreate
from backend.services.mail import MailService, Mail
from backend.tables import auth_user, activation_link
from backend.config import settings
from auth.auth import authenticate_user, hash_password, create_access_token, decode_token


BACKEND_URL = settings.backend_url


class AuthService:
    def __init__(self,
            conn: Connection,
            mail_service: MailService,
            uuid_factory: Callable[[], UUID],
    ) -> None:
        self.conn = conn
        self.mail_service = mail_service
        self.uuid_factory = uuid_factory

    def _send_activation_link(self, user_id):
        code = token_urlsafe()
        self.conn.execute(
            insert(activation_link)
            .values({
                "user_id": user_id,
                "code": code,
            })
        )
        mail = Mail(
            from_addr="test@test.com",
            to_addr="to@test.com",
            subject="Activate Account",
            content=f"{BACKEND_URL}/register/activate/{code}"
        )
        self.mail_service.send_mail(mail)

    def create_auth_user(self, auth_create: AuthCreate):
        hashed_password = hash_password(auth_create.password)
        row = self.conn.execute(
            insert(auth_user)
            .values({
                "public_id": self.uuid_factory(),
                "hashed_password": hashed_password,
                **auth_create.model_dump(exclude={"password"})
            })
            .returning(auth_user)
        ).first()
        auth_db = AuthDB.model_validate(row, from_attributes=True)
        if not auth_db.active:
            self._send_activation_link(auth_db.id)
        return auth_db
    
    def get_code_for_user(self, user_id: int) -> str | None:
        code = self.conn.scalar(
            select(activation_link.c.code)
            .where(activation_link.c.user_id == user_id)
        )
        if code:
            return str(code)
        else:
            return None

    def activate_account(self, code: str):
        activated_user_id = self.conn.scalar(
            delete(activation_link)
            .where(activation_link.c.code == code)
            .returning(activation_link.c.user_id)
        )
        assert activated_user_id
        self.conn.execute(
            update(auth_user)
            .where(auth_user.c.id == activated_user_id)
            .values(active=True)
        )

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