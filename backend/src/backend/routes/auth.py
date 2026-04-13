from fastapi import Depends, HTTPException, Path
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.services.auth import AuthService
from backend.services.user import UserService
from backend.services.organization import OrganizationService
from backend.schemas.token import TokenCreate
from backend.dependencies import (
    get_auth_service,
    get_user_service,
    get_organization_service,
)


router = APIRouter()


@router.post("/token")
def token_route(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(get_auth_service),
        user_service: UserService = Depends(get_user_service),
        organization_service: OrganizationService = Depends(get_organization_service),
):
    if auth_service.login(form_data.username, form_data.password):
        auth_user_db = auth_service.get_auth_user(form_data.username)
        if auth_user_db.entity_type == "user":
            entity_db = user_service.get_user(id=auth_user_db.id)
        else:
            entity_db = organization_service.get_organization(id=auth_user_db.id)
        access_token = auth_service.create_access_token(TokenCreate(
            sub=form_data.username,
            entity_type=auth_user_db.entity_type,
            active=auth_user_db.active,
            **entity_db.model_dump(exclude={"id"}),
        ))
        return {"access_token": access_token, "token_type": "bearer"} # TODO: Put in Pydantic schema
    else:
        raise HTTPException(status_code=401)


@router.post("/register/activate/{code}", status_code=204)
def activate_account_route(
        code: str = Path(),
        auth_service: AuthService = Depends(get_auth_service),
):
    auth_service.activate_account(code)