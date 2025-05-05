from auth.src.services.auth.dto import UserCreateDTO
from src.services.auth.token_service import TokenService
from src.services.auth.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService, token_service: TokenService):
        self.user_service = user_service
        self.token_service = token_service

    async def registration(self, data: UserCreateDTO):
        new_user = await self.user_service.create_user(data=data)
