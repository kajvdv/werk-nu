from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, Connection

from api.database import get_conn
from api.tables import vacancy
from api.schemas.vacancy import VacancyPublic, VacancyCreate


router = APIRouter()


@router.get("")
def get_vacancies_of_org_route(organization: str):
    return []


@router.post("", response_model=VacancyPublic)
def post_vacancy_route(
    organization: str,
    vacancy_data: VacancyCreate,
    session: Connection = Depends(get_conn)
):
    stmt = (
        insert(vacancy)
        .values(**vacancy_data.model_dump())
        .returning(vacancy.c.id)
    )
    id = session.scalar(stmt)
    session.commit()
    return {
        "id": str(id),
        "title": "test",
        "organization": organization
    }