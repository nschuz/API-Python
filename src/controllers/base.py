from typing import Generic, TypeVar

from sqlalchemy.orm.session import Session

from models.base import BaseModel


Model = TypeVar("Model", bound=BaseModel)


class Controller(Generic[Model]):

    def __init__(self, session: Session):
        self.session = session
        self.model: type[Model] = type(Model)

    def get(self, pk: int) -> Model:
        return self.session.get(self.model, pk)