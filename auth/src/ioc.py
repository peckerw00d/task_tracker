from typing import AsyncIterable
from dishka import Provider, Scope, from_context, provide

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.repository import RepositoryInterface, UserRepository
from src.db.database import new_session_maker
from src.config import Config


class DBProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_session_maker(
        self, config: Config
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_repo(self, session: AsyncSession) -> RepositoryInterface:
        return UserRepository(session=session)
