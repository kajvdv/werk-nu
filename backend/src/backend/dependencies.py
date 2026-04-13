from typing import Callable
import uuid
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import Connection

from backend.database import get_conn
from backend.schemas.user import UserPublic
from backend.schemas.organization import OrganizationPublic
from backend.services.organization import OrganizationService
from backend.services.user import UserService
from backend.services.vacancy import VacancyService
from backend.services.message import MessageService
from backend.services.auth import AuthService
from backend.services.mail import MailService
from auth import oauth2_scheme
from auth.auth import decode_token


def get_uuid_factory():
    return uuid.uuid4


def get_current_user(token = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload['active']:
        raise HTTPException(status_code=401)
    return UserPublic.model_validate(payload, by_name=True)


def get_current_organization(token = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload['entity_type'] != "organization":
        raise HTTPException(status_code=400, detail="Not an organization")
    return OrganizationPublic.model_validate(payload, by_name=True)


def get_mail_service():
    return MailService()


def get_auth_service(
        conn: Connection = Depends(get_conn),
        mail_service: MailService = Depends(get_mail_service),
        uuid_factory: Callable[[], UUID] = Depends(get_uuid_factory)
):
    return AuthService(conn, mail_service, uuid_factory)
    

def get_organization_service(
        conn: Connection = Depends(get_conn),
        auth_service: AuthService = Depends(get_auth_service),
):
    return OrganizationService(conn, auth_service)


def get_vacancy_service(
        conn: Connection = Depends(get_conn),
        organization_service = Depends(get_organization_service),
        uuid_factory: Callable[[], UUID] = Depends(get_uuid_factory),
):
    return VacancyService(conn, organization_service, uuid_factory)


def get_user_service(
        conn: Connection = Depends(get_conn),
        auth_service: AuthService = Depends(get_auth_service),
): 
    return UserService(conn, auth_service)


def get_message_service(
        conn: Connection = Depends(get_conn),
):
    return MessageService(conn)