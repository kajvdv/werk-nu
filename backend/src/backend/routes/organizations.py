from fastapi import APIRouter, Depends

from backend.schemas.organization import OrganizationCreate, OrganizationPublic
from backend.services.organization import OrganizationService

from backend.dependencies import (
    get_organization_service,
)


router = APIRouter()


@router.post('', status_code=201, response_model=OrganizationPublic)
def register_organization_route(
        organization_data: OrganizationCreate,
        organization_service: OrganizationService = Depends(get_organization_service)
):
    org_db = organization_service.create_organization(organization_data)
    return OrganizationPublic.model_validate(org_db, from_attributes=True)