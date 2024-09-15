from pydantic import Extra
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_NAME: str = "db"
    DB_USER: str = "test_user"
    DB_PASSWORD: str = "test_pass"

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class LoggingSettings(BaseSettings):
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "app.log"
    LOG_ENCODING: str = "utf-8"

class Auth(BaseSettings):
    USERNAME: str = "Misha"
    PASSWORD: str = "misha_coder_911"

class ImagePath(BaseSettings):
    IMAGE_PATH: str = r"C:\Users\Aleksandr Riabinskii\Documents\TevianTest\src\db\Images"

class AuthTevianSwagger(BaseSettings):
    TEVIAN_SWAGGER_EMAIL: str = "olexander.rabota@yandex.ru"
    TEVIAN_SWAGGER_PASSWORD: str = "password"

class Settings(APISettings, DatabaseSettings, LoggingSettings, Auth, ImagePath, AuthTevianSwagger):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
