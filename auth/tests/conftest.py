import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.users import User
from src.db.repository import UserRepository


@pytest_asyncio.fixture(scope="function")
async def mock_async_session():
    session = AsyncMock(spec=AsyncSession)

    session.execute = AsyncMock(
        return_value=MagicMock(
            scalars=MagicMock(
                return_valute=MagicMock(first=MagicMock(return_value=None))
            )
        )
    )
    session.add = MagicMock()
    session.flush = AsyncMock()

    return session


@pytest_asyncio.fixture(scope="function")
async def user_repo(mock_async_session):
    return UserRepository(session=mock_async_session)


@pytest_asyncio.fixture(scope="function")
async def test_user():
    return User(
        id="123", username="User202", email="example@example.com", password="qwerty"
    )
