import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, Connection

from backend.database import get_conn
from backend.tables import vacancy, organization
from backend.schemas.vacancy import VacancyPublic, VacancyCreate, VacancyPublicOwn
from backend.schemas.organization import OrganizationPublic
from backend.services.vacancy import VacancyService
from backend.services.organization import OrganizationService
from backend.dependencies import (
    get_vacancy_service,
    get_organization_service,
    get_current_organization,
)


router = APIRouter()


@router.get("", response_model=list[VacancyPublic])
def get_vacancies_route(
        vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    vacancies = vacancy_service.get_vacancies()
    return [
        vacancy_service.publify_vacancy(vacancy)
        for vacancy in vacancies
    ]


@router.get("/me", response_model=list[VacancyPublicOwn])
def get_own_vacancies(
        organization: OrganizationPublic = Depends(get_current_organization),
        vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    vacancies = vacancy_service.get_vacancies(org_public_id=organization.id)
    return [
        vacancy_service.publify_own_vacancy(vacancy)
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


@router.delete("/{vacancy_id}", status_code=204)
def delete_vacancy_route(
        vacancy_id: str,
        organization: OrganizationPublic = Depends(get_current_organization),
        vacancy_service: VacancyService = Depends(get_vacancy_service),
        organization_service: OrganizationService = Depends(get_organization_service)
):
    vacancy_db = vacancy_service.get_vacancy_by_pulic_id(uuid.UUID(vacancy_id))
    organization_db = organization_service.get_organization(public_id=organization.id)
    if vacancy_db.organization_id != organization_db.id:
        raise HTTPException(status_code=401)
    vacancy_service.delete_vacancy(vacancy_db)