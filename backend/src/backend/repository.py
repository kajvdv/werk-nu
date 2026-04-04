from typing import Protocol, Self


class Model(Protocol):
    def update(self, model: Self) -> None: ... 


class Repository(Protocol):
    def get(self, id) -> Model: ...
    def delete(self, model: Model) -> None: ...