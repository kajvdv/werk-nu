from uuid import UUID

from sqlalchemy import select

from api.tables import organization, auth_user


def select_organization(*,
        id: int | None = None,
        public_id: UUID | None = None,
        select_columns = None
):
    stmt = (
        select(organization, auth_user)
        .join(auth_user, organization.c.id == auth_user.c.id)
    )
    if id:
        stmt = stmt.where(organization.c.id == id)
    elif public_id:
        stmt = stmt.where(auth_user.c.public_id == public_id)
    return stmt