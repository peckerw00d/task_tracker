from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.services.auth.dto import UserResponseDTO
from .base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)

    def to_response_dto(self) -> UserResponseDTO:
        return UserResponseDTO(id=self.id, username=self.username, email=self.email)
