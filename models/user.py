from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class UserProfile(Base):
    __tablename__ = "UserProfile"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    yandex_access_token: Mapped[Optional[str]]
    google_access_token: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    name: Mapped[Optional[str]]

