from os import environ as env

from pydantic import BaseModel, Field


class PostgresConfig(BaseModel):
    url: str = Field(alias="DB_URL")
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
