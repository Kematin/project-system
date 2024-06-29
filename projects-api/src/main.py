from contextlib import asynccontextmanager

import uvicorn
from admin.admin import admin_router
from bot.bot import bot_router
from database import init_models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger


def create_logger() -> None:
    logger.add(
        "logs/debug.log",
        format="{time} {level} {message}",
        level="INFO",
        rotation="150 KB",
        compression="zip",
    )
    logger.info("Start app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_logger()
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(admin_router, prefix="/admin")
app.include_router(bot_router, prefix="/bot")

origins = ["http://kematin.space:8787"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stop app")
