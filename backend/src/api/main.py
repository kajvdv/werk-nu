from fastapi import FastAPI

from api.routes.users import router as users_router
from api.routes.vacancies import router as vacancies_router
from api.routes.applications import router as applications_router


app = FastAPI()

app.include_router(vacancies_router,    prefix="/{organization}/vacancies")
app.include_router(applications_router, prefix="/{organization}/vacancies/{vacancy_id}/applications")
app.include_router(users_router,        prefix="/users")
