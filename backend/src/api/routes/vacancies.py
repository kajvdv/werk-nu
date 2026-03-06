from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, Connection

from api.database import get_conn
from api.tables import vacancy, organization
from api.schemas.vacancy import VacancyPublic, VacancyCreate


router = APIRouter()


@router.get("")
def get_vacancies_of_org_route(organization: str):
    return []


@router.post("", response_model=VacancyPublic)
def post_vacancy_route(
    # organization: str,
    vacancy_data: VacancyCreate,
    connection: Connection = Depends(get_conn),
):
    stmt = (
        select(organization.c.id)
        .where(organization.c.public_id == vacancy_data.organization_id)
    )
    organization_id = connection.execute(stmt).scalar()
    stmt = (
        insert(vacancy)
        .values(
            organization_id=organization_id,
            **vacancy_data.model_dump(exclude={"organization_id"})
        )
        .returning(
            vacancy.c.public_id,
        )
    )
    public_id = connection.scalar(stmt)
    connection.commit()
    return {
        "public_id": public_id,
        "title": "test",
        "organization_id": vacancy_data.organization_id
    }