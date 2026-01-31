from pydantic_settings import BaseSettings
from pydantic import PostgresDsn



class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_URL: str
    STRIPE_PRICE_ID: str
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    PLAN_PRICE_ID: str
    DOMAIN: str

    class Config:
        env_file = ".env"

settings = Settings()
