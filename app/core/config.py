from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    # Database settings
    database_url: str = "sqlite:///./employee_search.db"
    
    # API settings
    api_v1_prefix: str = "/api/v1"


settings = Settings()

