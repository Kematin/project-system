from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    JWT_SECRET_KEY: str
    BOT_SECRET_KEY: str
    DATABASE_URL: str
    CATEGORIES: dict = Field({"full11": 1, "full9": 2, "minimum": 3, "exclusive": 4})
    FILE_TYPES: dict = Field(
        {
            "doc": "document.docx",
            "pptx": "presentation.pptx",
            "png": "unique.png",
            "cover": "cover.png",
            "product": "product",
        }
    )
    PROJECT_FIELDS: dict = Field(
        {"pptx": "have_presentation", "png": "have_unique", "product": "have_product"}
    )
    MEDIA_TYPES: dict = Field(
        {
            "doc": "application/msword",
            "pptx": "application/vnd.ms-powerpoint",
            "png": "image/png",
            "cover": "image/png",
            "product": "application/zip",
        }
    )

    class Config:
        env_file = ".env"


config = Settings()
