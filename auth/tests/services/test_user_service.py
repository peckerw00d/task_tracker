import pytest

from src.services.auth.dto import UserResponseDTO


@pytest.mark.asyncio
async def test_user_service_create(
    test_user, test_user_dto, user_service, mock_user_repository
):
    result = await user_service.create_user(test_user_dto)

    mock_user_repository.create.assert_awaited_once()

    assert result == test_user.to_response_dto()
