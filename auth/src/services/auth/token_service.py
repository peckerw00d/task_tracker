from datetime import datetime, timedelta, timezone
import time
from jose import jwt, exceptions

from src.config import SecurityConfig


class TokenService:
    def __init__(self, security_config: SecurityConfig):
        self.security_config = security_config

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode,
            self.security_config.secret_key,
            algorithm=self.security_config.algorithm,
        )
        return encode_jwt

    async def validate_token(self, token: str):
        try:
            payload = jwt.decode(
                token,
                self.security_config.secret_key,
                algorithms=[self.security_config.algorithm],
            )

        except exceptions.ExpiredSignatureError:
            raise ValueError("Token expired")

        except exceptions.JWSSignatureError:
            raise ValueError("Invalid token signature")

        return payload
