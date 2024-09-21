from typing import List
from sqlalchemy.orm import Mapped, relationship
from . import Config


class Author(Config.BASE):
    name: Mapped[str]
    tours : Mapped[List["Tour"]] = relationship(back_populates="author")