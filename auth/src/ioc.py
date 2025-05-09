from typing import AsyncIterable
from dishka import Provider, Scope, from_context, provide

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.services.auth.auth_service import AuthService
from src.services.auth.user_service import UserService
from src.services.auth.token_service import TokenService
from src.db.repository import RepositoryInterface, UserRepository
from src.db.database import new_session_maker
from src.config import Config, SecurityConfig


class DBProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_session_maker(
        self, config: Config
    ) -> async_sessionmaker[AsyncSession]:
        return await new_session_maker(config.postgres)

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


class SecurityProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_security_config(self) -> SecurityConfig:
        return SecurityConfig()

    @provide(scope=Scope.REQUEST)
    async def get_token_service(self, security_config: SecurityConfig) -> TokenService:
        return TokenService(security_config=security_config)

    @provide(scope=Scope.REQUEST)
    async def get_user_service(self, repo: RepositoryInterface) -> UserService:
        return UserService(repo=repo)

    @provide(scope=Scope.REQUEST)
    async def get_auth_service(
        self,
        user_service: UserService,
        token_service: TokenService,
        repo: RepositoryInterface,
    ) -> AuthService:
        return AuthService(
            user_service=user_service, token_service=token_service, repo=repo
        )
