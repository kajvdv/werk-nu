from fastapi import FastAPI

from backend.routes.users import router as users_router
from backend.routes.vacancies import router as vacancies_router
from backend.routes.applications import router as applications_router
from backend.routes.auth import router as auth_router
from backend.routes.organizations import router as organization_router


app = FastAPI()

app.include_router(vacancies_router,    prefix="/vacancies")
app.include_router(applications_router, prefix="/vacancies/{vacancy_id}/applications")
app.include_router(users_router,        prefix="/users")
app.include_router(organization_router, prefix="/organizations")
app.include_router(auth_router,         prefix="")
