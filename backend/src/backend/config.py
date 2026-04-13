from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    
    backend_url: str = Field(init=False)
    database_url: str = Field(init=False)


settings = Settings()