from unittest.mock import AsyncMock
import pytest

from src.services.auth.exceptions import UsernameAlreadyInUse
from src.services.auth.dto import UserResponseDTO


@pytest.mark.asyncio
async def test_user_service_create_success(
    test_user, test_user_dto, user_service, mock_user_repository
):
    mock_user_repository.get_by_username = AsyncMock(return_value=None)
    mock_user_repository.get_by_email = AsyncMock(return_value=None)
    mock_user_repository.create = AsyncMock(return_value=test_user)

    result = await user_service.create_user(test_user_dto)

    mock_user_repository.get_by_username.assert_awaited_once_with(
        username=test_user_dto.username
    )
    mock_user_repository.get_by_email.assert_awaited_once_with(
        email=test_user_dto.email
    )
    mock_user_repository.create.assert_awaited_once()

    assert result == test_user.to_response_dto()


@pytest.mark.asyncio
async def test_user_service_create_both_username_and_email_already_exists(
    test_user_dto, user_service, mock_user_repository
):
    mock_user_repository.get_by_username = AsyncMock(return_value=test_user_dto)
    mock_user_repository.get_by_email = AsyncMock(return_value=test_user_dto)

    with pytest.raises(UsernameAlreadyInUse):
        await user_service.create_user(test_user_dto)

    mock_user_repository.create.assert_not_awaited()
