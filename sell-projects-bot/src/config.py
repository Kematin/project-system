from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    SECRET_KEY: str
    ADMIN_IP: int
    PROVIDER_TOKEN: str
    WEBHOOCK_NGROK: str
    CATEGORIES: dict = Field({1: "Full 11", 2: "Full 9", 3: "Minimum", 4: "Exclusive"})

    class Config:
        env_file = ".env"


config = Settings()
