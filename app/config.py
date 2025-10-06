from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
from urllib.parse import urlparse


class Settings(BaseSettings):
    # Map to common uppercase environment variables used by hosting providers
    # Make individual DB fields optional — if a DATABASE_URL is provided we will
    # parse and populate them so the rest of the code can continue to read
    # settings.database_hostname, settings.database_username, etc.
    database_hostname: Optional[str] = Field(None, env="DATABASE_HOSTNAME")
    database_port: Optional[str] = Field(None, env="DATABASE_PORT")
    database_password: Optional[str] = Field(None, env="DATABASE_PASSWORD")
    database_name: Optional[str] = Field(None, env="DATABASE_NAME")
    database_username: Optional[str] = Field(None, env="DATABASE_USERNAME")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    # Optional single URL (e.g. provided by Render, Heroku, Railway):
    database_url: Optional[str] = Field(None, env="DATABASE_URL")

    class Config:
        env_file = ".env"

    def model_post_init(self, __context):
        # If a DATABASE_URL is provided, parse it and fill missing DB_* fields.
        if self.database_url:
            parsed = urlparse(self.database_url)
            # netloc -> user:pass@host:port
            if not self.database_username:
                self.database_username = parsed.username
            if not self.database_password:
                self.database_password = parsed.password
            if not self.database_hostname:
                self.database_hostname = parsed.hostname
            if not self.database_port and parsed.port:
                self.database_port = str(parsed.port)
            # path may start with '/', strip it
            if not self.database_name:
                path = parsed.path.lstrip('/') if parsed.path else None
                self.database_name = path

        # If DATABASE_URL was not provided, ensure individual DB_* are present.
        if not self.database_url:
            missing = []
            for field in (
                'database_hostname',
                'database_port',
                'database_password',
                'database_name',
                'database_username',
            ):
                if getattr(self, field) is None:
                    missing.append(field)
            if missing:
                raise ValueError(f"Missing required database settings: {', '.join(missing)}")


settings = Settings()