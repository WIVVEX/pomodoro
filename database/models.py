from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr

from typing import Any, Optional


class Base(DeclarativeBase):
    id: Any
    __name__: str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

class Tasks(Base):
    __tablename__ = "Tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]

class Categories(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Optional[str]]
    name: Mapped[str]