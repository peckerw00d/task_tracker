from os import getenv

from pydantic import BaseModel, Field


class SecurityConfig(BaseModel):
    algorithm: str = getenv("ALGORITHM")
    secret_key: str = getenv("SECRET_KEY")


class PostgresConfig(BaseModel):
    url: str = str(getenv("AUTH_DB_URL"))
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig())
    security: SecurityConfig = Field(default_factory=lambda: SecurityConfig())
