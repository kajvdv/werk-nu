from fastapi import APIRouter, Depends, Path
from sqlalchemy import select, insert, Connection

from api.schemas.applicant import ApplicantPublic
from api.schemas.vacancy import VacancyDB
from api.tables import application, user
from api.dependencies.vacancy import get_vacancy
from api.database import get_conn
from api.deps import (
    get_current_user,
    get_vacancy_service,
    get_user_service,
)


router = APIRouter()


@router.post("", response_model=ApplicantPublic)
def post_application(
        user_public = Depends(get_current_user),
        vacancy_service = Depends(get_vacancy_service),
        user_service = Depends(get_user_service),
        vacancy_id = Path()
):
    user_db = user_service.get_user(user_public)
    vacancy_db = vacancy_service.get_vacancy_by_pulic_id(vacancy_id)
    return vacancy_service.apply(user_db, vacancy_db)
    # return ApplicantPublic.model_validate({
    #     "user": user_db.model_dump(),
    #     "vacancy": vacancy_db.model_dump()
    # })

@router.get("", response_model=list[ApplicantPublic])
def get_applications(
        vacancy_db: VacancyDB = Depends(get_vacancy),
        # vacancy_id: int = Path(),
        conn: Connection = Depends(get_conn)
):
    stmt = (
        select(user)
        .join(application, application.c.user_id == user.c.id)
        .where(application.c.vacancy_id == vacancy_db.id)
    )
    rows = conn.execute(stmt)
    return [{
        "user": row,
        "vacancy": vacancy_db
    } for row in rows]