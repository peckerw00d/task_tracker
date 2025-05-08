import pytest
from sqlalchemy import select

from src.db.models import User


@pytest.mark.asyncio
async def test_repository_create(user_repo, test_user, mock_async_session):
    result = await user_repo.create(test_user)

    mock_async_session.add.assert_called_once_with(test_user)
    mock_async_session.flush.assert_awaited_once()

    assert result is test_user


@pytest.mark.asyncio
async def test_repository_get_user(user_repo, test_user, mock_async_session):
    mock_async_session.execute.return_value.scalars.return_value.first.return_value = (
        test_user
    )

    result = await user_repo.get("123")

    actual_query = str(mock_async_session.execute.await_args[0][0])
    expected_query = str(select(User).where(User.id == "123"))

    assert actual_query == expected_query
    assert result == test_user


@pytest.mark.asyncio
async def test_repository_get_user_not_found(user_repo, mock_async_session):
    mock_async_session.execute.return_value.scalars.return_value.first.return_value = (
        None
    )

    result = await user_repo.get("123")

    assert result is None
    mock_async_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_repository_get_by_username(user_repo, test_user, mock_async_session):
    mock_async_session.execute.return_value.scalars.return_value.first.return_value = (
        test_user
    )

    result = await user_repo.get_by_username("User202")

    actual_query = str(mock_async_session.execute.await_args[0][0])
    expected_query = str(select(User).where(User.username == "User202"))
    assert actual_query == expected_query
    assert result == test_user
