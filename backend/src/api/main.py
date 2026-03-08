from fastapi import FastAPI

from api.routes.users import router as users_router
from api.routes.vacancies import router as vacancies_router
from api.routes.applications import router as applications_router
from api.routes.auth import router as auth_router
from api.routes.organizations import router as organization_router


app = FastAPI()

app.include_router(vacancies_router,    prefix="/{organization_id}/vacancies")
app.include_router(applications_router, prefix="/{organization_id}/vacancies/{vacancy_id}/applications")
app.include_router(users_router,        prefix="/users")
app.include_router(organization_router, prefix="/organizations")
app.include_router(auth_router,         prefix="")
