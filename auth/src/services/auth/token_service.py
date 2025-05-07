from datetime import datetime, timedelta, timezone
from jose import jwt

from src.config import SecurityConfig


class TokenService:
    def __init__(self, security_config: SecurityConfig):
        self.security_config = security_config

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode,
            self.security_config.secret_key,
            algorithm=self.security_config.algorithm,
        )
        return encode_jwt
