from fastapi import APIRouter, Depends, Path

from api.schemas.applicant import ApplicantPublic
from api.schemas.user import UserPublic
from api.services.vacancy import VacancyService
from api.services.user import UserService
from api.dependencies import (
    get_current_user,
    get_vacancy_service,
    get_user_service,
)


router = APIRouter()


@router.post("", response_model=ApplicantPublic)
def post_application(
        user_public: UserPublic = Depends(get_current_user),
        vacancy_service: VacancyService = Depends(get_vacancy_service),
        user_service: UserService = Depends(get_user_service),
        vacancy_id = Path()
):
    user_db = user_service.get_user(public_id=user_public.id)
    vacancy_db = vacancy_service.get_vacancy_by_pulic_id(vacancy_id)
    return vacancy_service.apply(user_db, vacancy_db)


@router.get("", response_model=list[ApplicantPublic])
def get_applications(
        vacancy_service: VacancyService = Depends(get_vacancy_service),
        vacancy_id = Path()
):
    vacancy_db = vacancy_service.get_vacancy_by_pulic_id(vacancy_id)
    return vacancy_service.get_applications(vacancy_db)