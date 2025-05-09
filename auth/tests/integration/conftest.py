from os import getenv
from dotenv import load_dotenv

import pytest_asyncio

from httpx import AsyncClient

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import Config, PostgresConfig
from src.db.models.base import Base
from src.main import app


load_dotenv()

TEST_DB_URL = getenv("AUTH_TEST_DB_URL")


@pytest_asyncio.fixture(scope="session")
async def test_config():
    return Config(postgres=PostgresConfig(url=TEST_DB_URL))


@pytest_asyncio.fixture(scope="session", autouse=True)
async def engine():
    engine = create_async_engine(url=TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session_factory(engine):
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_factory


@pytest_asyncio.fixture(scope="function")
async def session(session_factory):
    async with session_factory() as session:
        async with session.begin():
            yield session


@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client
