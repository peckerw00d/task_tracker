from dotenv import load_dotenv
from fastapi import FastAPI

from dishka import make_async_container

import uvicorn

from src.config import Config
from src.ioc import AppProvider


load_dotenv()


config = Config()
container = make_async_container(AppProvider(), context={Config: config})

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
