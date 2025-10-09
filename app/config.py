from pydantic import Field, field_validator
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
    # Default to HS256 if the host doesn't provide an algorithm value.
    # Some hosting UIs set an unset variable to strings like 'false' — we
    # normalize those to None and then fall back to this default.
    algorithm: str = Field("HS256", env="ALGORITHM")
    # Accept numeric values for the token expiry. Provide a safe default (30 minutes)
    # and coerce common env string representations. This prevents a hard failure when
    # a hosting UI accidentally sets the variable to a non-numeric value like "false".
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
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

    # Coerce and validate `access_token_expire_minutes` from environment values.
    @field_validator('access_token_expire_minutes', mode='before')
    def _coerce_access_token_expire_minutes(cls, v):
        # If none provided, use default (already set by Field)
        if v is None:
            return 30
        # If already an int, accept it
        if isinstance(v, int):
            return v
        # Booleans can come through in some environment systems; treat True=1, False=0
        if isinstance(v, bool):
            return 1 if v else 0
        # Strings: try to parse as integer, fallback to default if not numeric
        if isinstance(v, str):
            s = v.strip()
            # common case: numeric string
            if s.lstrip('-').isdigit():
                return int(s)
            # try float-ish strings like '30.0'
            try:
                f = float(s)
                return int(f)
            except Exception:
                # handle 'true'/'false' or other non-numeric values by falling back to default
                return 30
        # Anything else: return default
        return 30
    
    @field_validator('database_url', mode='before')
    def _normalize_database_url(cls, v):
        # Some hosting UIs may set an unset/disabled env var to string values like
        # "false", "None", or "0". Treat those as not provided (None) so the
        # app can fall back to DB_* fields or raise a clearer error later.
        if v is None:
            return None
        if isinstance(v, str):
            s = v.strip()
            if s == "":
                return None
            if s.lower() in ("false", "none", "null", "0"):
                return None
            return s
        return v

    @field_validator('algorithm', mode='before')
    def _normalize_algorithm(cls, v):
        # Treat empty or common 'false' tokens as not provided so the
        # default value can be used instead of passing 'false' to jose.
        if v is None:
            return None
        if isinstance(v, str):
            s = v.strip()
            if s == "":
                return None
            if s.lower() in ("false", "none", "null", "0"):
                return None
            return s
        return v


settings = Settings()