from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from database import Base


class Tasks(Base):
    __tablename__ = "Tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfile.id"), nullable=False)

class Categories(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Optional[str]]
    name: Mapped[str]