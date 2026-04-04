import uuid
from typing import Callable
from uuid import UUID

from sqlalchemy import Connection, select, insert

from backend.schemas.vacancy import VacancyCreate, VacancyDB, VacancyPublic
from backend.schemas.user import UserDB, UserPublic
from backend.schemas.applicant import ApplicantPublic
from backend.queries.user import select_user
from backend.queries.organization import select_organization
from backend.tables import vacancy, organization, application, user

from .organization import OrganizationService


class VacancyService:
    def __init__(self,
            conn: Connection,
            organization_service: OrganizationService,
            uuid_factory: Callable[[], UUID] = uuid.uuid4,
    ) -> None:
        self.conn = conn
        self.organization_service = organization_service
        self.uuid_factory = uuid_factory

    # I don't like this method. Services should return public schemas.
    def publify_vacancy(self, vacancy_db: VacancyDB) -> VacancyPublic:
        # TODO: Put this into the organization service
        organization_id = self.conn.execute(select_organization(id=vacancy_db.organization_id)).first()
        return VacancyPublic.model_validate({
            "organization_id": organization_id.public_id,
            **vacancy_db.model_dump(exclude={"organization_id"})
        })

    def get_vacancies(self):
        stmt = (
            select(vacancy)
        )
        rows = self.conn.execute(stmt)
        return [
            VacancyDB.model_validate(row, from_attributes=True)
            for row in rows
        ]


    def create_vacancy(self, data: VacancyCreate, public_organization_id: UUID):
        organization_id = self.conn.scalar(select_organization(public_id=public_organization_id))
        stmt = (
            insert(vacancy)
            .values({
                "public_id": self.uuid_factory(),
                "organization_id": organization_id,
                **data.model_dump(exclude={"organization_id"}),
            })
            .returning(vacancy)
        )
        row = self.conn.execute(stmt).first()
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
        # TODO: Put this into the organization service
        organization = self.conn.execute(select_organization(
            id=vacancy_db.organization_id
        )).first()
        return ApplicantPublic.model_validate({
            "user": user_db.model_dump(),
            "vacancy": VacancyPublic.model_validate({
                "organization_id": organization.public_id,
                **vacancy_db.model_dump(exclude={"organization_id"})
            }),
        })

    def get_applications(self, vacancy_db: VacancyDB) -> list[ApplicantPublic]:
        rows = self.conn.execute(
            select_user()
            .join(application, user.c.id == application.c.user_id)
            .where(application.c.vacancy_id == vacancy_db.id)
        )
        # TODO: Put this into the organization service
        organization = self.conn.execute(select_organization(
            id=vacancy_db.organization_id
        )).first()
        return [
            ApplicantPublic.model_validate({
                "user": UserPublic.model_validate(row, from_attributes=True),
                "vacancy": VacancyPublic.model_validate({
                    "organization_id": organization.public_id,
                    **vacancy_db.model_dump(exclude={"organization_id"})
                }),
            })
            for row in rows
        ]
