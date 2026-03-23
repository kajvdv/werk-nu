from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, Connection

from backend.database import get_conn
from backend.tables import vacancy, organization
from backend.schemas.vacancy import VacancyPublic, VacancyCreate
from backend.schemas.organization import OrganizationPublic
from backend.services.vacancy import VacancyService
from backend.dependencies import (
    get_vacancy_service,
    get_current_organization,
)


router = APIRouter()


@router.get("")
def get_vacancies_route(
        vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    vacancies = vacancy_service.get_vacancies()
    return [
        vacancy_service.publify_vacancy(vacancy)
        for vacancy in vacancies
    ]


@router.get("/{organization_id}")
def get_vacancies_of_org_route(organization: str):
    return []


@router.post("", response_model=VacancyPublic, status_code=201)
def post_vacancy_route(
        vacancy_data: VacancyCreate,
        organization: OrganizationPublic = Depends(get_current_organization),
        vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    vacancy_db = vacancy_service.create_vacancy(vacancy_data, organization.id)
    return vacancy_service.publify_vacancy(vacancy_db)