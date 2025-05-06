from abc import abstractmethod
from typing import Optional, Protocol

from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.users import User


class RepositoryInterface(Protocol):
    @abstractmethod
    async def create(self, entity):
        raise NotImplementedError

    @abstractmethod
    async def get(self, entity_id):
        raise NotImplementedError


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> Optional[User]:
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_by_username(self, username: str):
        stmt = Select(User).where(User.username == username)
        result: Result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get(self, user_id: str) -> Optional[User]:
        stmt = Select(User).where(User.id == user_id)
        result: Result = await self.session.execute(stmt)
        return result.scalars().first()
