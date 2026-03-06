from uuid import UUID

from sqlalchemy import Connection, select, insert

from api.schemas.vacancy import VacancyCreate, VacancyDB, VacancyPublic
from api.schemas.user import UserDB, UserPublic
from api.schemas.applicant import ApplicantPublic
from api.tables import vacancy, organization, application, user

from .organization import OrganizationService


class VacancyService:
    def __init__(self,
            conn: Connection,
            organization_service: OrganizationService
    ) -> None:
        self.conn = conn
        self.organization_service = organization_service

    def create_vacancy(self, data: VacancyCreate):
        organization_id = self.conn.scalar(
            select(organization.c.id)
            .where(organization.c.public_id == data.organization_id)
        )
        stmt = (
            insert(vacancy)
            .values({
                "organization_id": organization_id,
                **data.model_dump(exclude={"organization_id"}),
            })
            .returning(vacancy)
        )
        row = self.conn.execute(stmt).first()
        self.conn.commit()
        return VacancyDB.model_validate(row, from_attributes=True)
    
    def get_vacancy_by_pulic_id(self, public_id: UUID) -> VacancyDB:
        stmt = (
            select(vacancy)
            .where(vacancy.c.public_id == public_id)
        )
        row = self.conn.execute(stmt).first()
        return VacancyDB.model_validate(row, from_attributes=True)

    def apply(self, user_db: UserDB, vacancy_db: VacancyDB) -> ApplicantPublic:
        self.conn.execute(
            insert(application)
            .values({
                "user_id": user_db.id,
                "vacancy_id": vacancy_db.id,
            })
        )
        self.conn.commit()
        # TODO: Put this into the organization service
        organization_id = self.conn.scalar(
            select(organization.c.public_id)
            .where(organization.c.id == vacancy_db.organization_id)
        )
        return ApplicantPublic.model_validate({
            "user": user_db.model_dump(),
            "vacancy": VacancyPublic.model_validate({
                "organization_id": organization_id,
                **vacancy_db.model_dump(exclude={"organization_id"})
            }),
        })

    def get_applications(self, vacancy_db: VacancyDB) -> list[ApplicantPublic]:
        rows = self.conn.execute(
            select(user)
            .join(application, user.c.id == application.c.user_id)
            .where(application.c.vacancy_id == vacancy_db.id)
        )
        # TODO: Put this into the organization service
        organization_id = self.conn.scalar(
            select(organization.c.public_id)
            .where(organization.c.id == vacancy_db.organization_id)
        )
        return [
            ApplicantPublic.model_validate({
                "user": UserPublic.model_validate(row, from_attributes=True),
                "vacancy": VacancyPublic.model_validate({
                    "organization_id": organization_id,
                    **vacancy_db.model_dump(exclude={"organization_id"})
                }),
            })
            for row in rows
        ]