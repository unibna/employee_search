from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    database_url: str = "sqlite:///./employee_search.db"
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

