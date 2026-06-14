from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    UPLOAD_DIR: str = "uploads_data"
    ADMIN_EMAIL: str = "soldartemetalorg@gmail.com"
    ADMIN_PASSWORD: str = "Admin123!"
    DEBUG: bool = True

    model_config = {"env_file": ".env"}

settings = Settings()
