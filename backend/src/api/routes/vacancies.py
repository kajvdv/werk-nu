from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, Connection

from api.database import get_conn
from api.tables import vacancy, organization
from api.schemas.vacancy import VacancyPublic, VacancyCreate
from api.schemas.organization import OrganizationPublic
from api.services.vacancy import VacancyService
from api.dependencies import (
    get_vacancy_service,
    get_current_organization,
)


router = APIRouter()


@router.get("")
def get_vacancies_of_org_route(organization: str):
    return []


@router.post("", response_model=VacancyPublic)
def post_vacancy_route(
    vacancy_data: VacancyCreate,
    organization: OrganizationPublic = Depends(get_current_organization),
    vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    vacancy_db = vacancy_service.create_vacancy(vacancy_data, organization.id)
    return vacancy_service.publify_vacancy(vacancy_db)