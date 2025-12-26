from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./portfolio.db"
    cache_dir: str = "./cache"
    cache_ttl_seconds: int = 3600


settings = Settings()
