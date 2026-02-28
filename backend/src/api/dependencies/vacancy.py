from fastapi import Depends
from sqlalchemy import select, Connection

from api.schemas.vacancy import VacancyDB
from api.tables import vacancy
from api.database import get_conn


def get_vacancy(
        vacancy_id: int,
        conn: Connection = Depends(get_conn)
    ) -> VacancyDB:
    stmt = (
        select(vacancy)
        .where(vacancy.c.id == vacancy_id)
    )
    row = conn.execute(stmt).first()
    if not row:
        raise LookupError("Vacancy not found")
    return VacancyDB.model_validate(row, from_attributes=True)
