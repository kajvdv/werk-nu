import uuid

from fastapi import Depends
from sqlalchemy import Connection

from api.database import get_conn
from api.schemas.user import UserPublic
from api.schemas.organization import OrganizationPublic
from api.services.organization import OrganizationService
from api.services.user import UserService
from api.services.vacancy import VacancyService
from api.services.message import MessageService
from api.services.auth import AuthService
from auth import oauth2_scheme
from auth.auth import decode_token


def get_current_user(token = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return UserPublic.model_validate(payload, by_name=True)


def get_current_organization(token = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return OrganizationPublic.model_validate(payload, by_name=True)


def get_auth_service(
        conn: Connection = Depends(get_conn),
):
    return AuthService(conn)
    

def get_organization_service(
        conn: Connection = Depends(get_conn),
        auth_service: AuthService = Depends(get_auth_service),
):
    return OrganizationService(conn, auth_service)


def get_vacancy_service(
        conn: Connection = Depends(get_conn),
        organization_service = Depends(get_organization_service)
):
    return VacancyService(conn, organization_service)


def get_user_service(
        conn: Connection = Depends(get_conn),
        auth_service: AuthService = Depends(get_auth_service),
): 
    return UserService(conn, auth_service)


def get_message_service(
        conn: Connection = Depends(get_conn),
):
    return MessageService(conn)