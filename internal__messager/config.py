from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AMQP_URI: str
    UNIQUE_PREFIX: str

    model_config = SettingsConfigDict(env_file=".env-internal")


settings = Settings()
