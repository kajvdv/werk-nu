from uuid import UUID

from sqlalchemy import select

from backend.tables import user, auth_user


def select_user(
        id: int | None = None,
        public_id: UUID | None = None,
):
    stmt = (
        select(user, auth_user)
        .join(auth_user, user.c.id == auth_user.c.id)
    )
    if id:
        stmt = stmt.where(user.c.id == id)
    elif public_id:
        stmt = stmt.where(auth_user.c.public_id == public_id)
    return stmt