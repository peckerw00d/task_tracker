from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka


import uvicorn

from src.config import Config
from src.ioc import DBProvider, RepositoryProvider, SecurityProvider
from src.api.routers import router


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


config = Config()
container = make_async_container(
    DBProvider(), RepositoryProvider(), SecurityProvider(), context={Config: config}
)

app = FastAPI(lifespan=lifespan)
app.include_router(router=router)

setup_dishka(container=container, app=app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
