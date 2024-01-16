from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AMQP_URI: str
    UNIQUE_PREFIX: str


settings = Settings()
