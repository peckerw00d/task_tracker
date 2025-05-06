from src.services.auth.exceptions import UserAlreadyExists, UsernameAlreadyInUse
from src.services.auth.password import get_password_hash
from src.db.models.users import User
from src.db.repository import RepositoryInterface
from src.services.auth.dto import UserCreateDTO, UserResponseDTO


class UserService:
    def __init__(self, repo: RepositoryInterface):
        self.repo = repo

    async def create_user(self, data: UserCreateDTO) -> UserResponseDTO:
        if await self.repo.get_by_username(username=data.username):
            raise UsernameAlreadyInUse

        if await self.repo.get_by_email(email=data.email):
            raise UserAlreadyExists

        password_hash = get_password_hash(data.password)

        user = User(
            username=data.username,
            email=data.email,
            password=password_hash,
        )
        created_user = await self.repo.create(user)

        return created_user.to_response_dto()
