from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AUTH_", extra="allow")
    
    secret_key_access: str = Field(init=False)
    secret_key_refresh: str = Field(init=False)


settings = Settings()