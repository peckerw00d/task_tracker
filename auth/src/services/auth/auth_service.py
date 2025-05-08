from src.services.auth.exceptions import InvalidCredentials
from src.services.auth.dto import UserCreateDTO, UserCredentialsDTO
from src.services.auth.token_service import TokenService
from src.services.auth.user_service import UserService
from src.services.auth.password import verify_password

from src.db.repository import RepositoryInterface


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        token_service: TokenService,
        repo: RepositoryInterface,
    ):
        self.user_service = user_service
        self.token_service = token_service
        self.repo = repo

    async def check_user_credentials(self, credentials: UserCredentialsDTO) -> bool:
        user = await self.repo.get_by_username(username=credentials.username)
        check_password = verify_password(
            plain_password=credentials.password, hash_password=user.password
        )

        if not (user or check_password):
            raise InvalidCredentials

        return True

    async def registration(self, data: UserCreateDTO) -> None:
        new_user = await self.user_service.create_user(data=data)

    async def login(self, credentials: UserCredentialsDTO):
        if await self.check_user_credentials(credentials=credentials):
            user = await self.repo.get_by_username(username=credentials.username)
            data = {"sub": str(user.id)}

            return await self.token_service.create_access_token(data=data)
