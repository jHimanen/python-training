from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str  # you can also use MySqlDsn for extra validation
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
DATABASE_URL = settings.database_url
