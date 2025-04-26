from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.config import PostgresConfig


async def new_session_maker(
    psql_config: PostgresConfig,
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(psql_config.url, pool_size=15, max_overflow=15)
    return async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )
