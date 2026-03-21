from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

from accept.domain.employer import Employer
from accept.domain.applicant import Applicant

if TYPE_CHECKING:
    from accept.drivers import Driver


class DriverFactory(Protocol):
    def create_driver(self) -> Driver:
        ...


class StoryTeller:
    def __init__(self, driver_factory: DriverFactory) -> None:
        self.driver_factory = driver_factory

    def spawn_employer(self,
        name: str,
        email: str,
        password: str,
    ):
        """Once upon a time there was an employer"""
        return Employer(
            self.driver_factory.create_driver(),
            name,
            email,
            password,
        )

    def spawn_applicant(self,
        name: str,
        email: str,
        password: str,
    ):
        return Applicant(
            self.driver_factory.create_driver(),
            name,
            email,
            password,
        )