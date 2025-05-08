import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth.dto import UserCreateDTO
from src.services.auth.user_service import UserService
from src.db.models.users import User
from src.db.repository import RepositoryInterface, UserRepository


@pytest_asyncio.fixture(scope="function")
async def mock_async_session():
    session = AsyncMock(spec=AsyncSession)

    session.execute = AsyncMock(
        return_value=MagicMock(
            scalars=MagicMock(
                return_value=MagicMock(first=MagicMock(return_value=None))
            )
        )
    )
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()

    return session


@pytest_asyncio.fixture(scope="function")
async def user_repo(mock_async_session):
    return UserRepository(session=mock_async_session)


@pytest_asyncio.fixture(scope="function")
async def test_user():
    return User(
        id="123", username="User202", email="example@example.com", password="qwerty"
    )


@pytest_asyncio.fixture(scope="function")
async def test_user_dto():
    return UserCreateDTO(
        username="User202", email="example@example.com", password="qwerty"
    )


@pytest_asyncio.fixture(scope="function")
async def mock_user_repository(test_user):
    repository = AsyncMock(spec=RepositoryInterface)
    repository.create = AsyncMock(return_value=test_user)
    repository.get = AsyncMock(return_value=test_user)

    return repository


@pytest_asyncio.fixture(scope="function")
async def user_service(mock_user_repository):
    return UserService(repo=mock_user_repository)
