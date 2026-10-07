from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://bugboard_user:bugboard_pass@postgres:5432/bugboard_db"
    UPLOAD_DIR: str = "./uploads"
    CORS_ORIGINS: str | list[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
