import uuid

from fastapi import Depends
from sqlalchemy import Connection

from api.database import get_conn
from api.schemas.user import UserPublic
from api.services.organization import OrganizationService
from api.services.user import UserService
from api.services.vacancy import VacancyService
from api.services.message import MessageService


def get_current_user():
    return UserPublic.model_validate({
        "name": "Test user",
        "public_id": uuid.uuid4()
    })
    

def get_organization_service(
        conn: Connection = Depends(get_conn)
):
    return OrganizationService(conn)


def get_vacancy_service(
        conn: Connection = Depends(get_conn),
        organization_service = Depends(get_organization_service)
):
    return VacancyService(conn, organization_service)


def get_user_service(
        conn: Connection = Depends(get_conn),
): 
    return UserService(conn)


def get_message_service(
        conn: Connection = Depends(get_conn),
):
    return MessageService(conn)