from fastapi import APIRouter, Depends, Path
from sqlalchemy import select, insert, Connection

from api.schemas.applicant import ApplicantPublic, ApplicationCreate
from api.schemas.vacancy import VacancyDB
from api.schemas.user import UserDB
from api.tables import application, user, vacancy
from api.dependencies.vacancy import get_vacancy
from api.dependencies.user import get_user
from api.database import get_conn


router = APIRouter()


@router.post("", response_model=ApplicantPublic)
def post_application(
    # application_data: ApplicationCreate,
    # vacancy_id: int
        vacancy: VacancyDB = Depends(get_vacancy),
        user: UserDB = Depends(get_user),
        conn: Connection = Depends(get_conn)
):
    stmt = (
        insert(application)
        .values({
            "vacancy_id": 1,
            "user_id": 1,
        })
    )
    conn.execute(stmt)
    conn.commit()
    return {
        "user": user.model_dump(),
        "vacancy": vacancy.model_dump()
    }

@router.get("", response_model=list[ApplicantPublic])
def get_applications(
        vacancy_db: VacancyDB = Depends(get_vacancy),
        # vacancy_id: int = Path(),
        conn: Connection = Depends(get_conn)
):
    stmt = (
        select(   
            user,    
        )
        .join(application, application.c.user_id == user.c.id)
        .where(application.c.vacancy_id == vacancy_db.id)
    )
    rows = conn.execute(stmt)
    return [{
        "user": row,
        "vacancy": vacancy_db
    } for row in rows]