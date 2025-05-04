from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

from src.config import SecurityConfig


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hash_password) -> bool:
    return pwd_context.verify(plain_password, hash_password)


class TokenService:
    def __init__(self, security_config: SecurityConfig):
        self.security_config = security_config

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode,
            self.security_config.secret_key,
            algorithm=self.security_config.algorithm,
        )
        return encode_jwt
