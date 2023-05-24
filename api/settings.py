from pydantic import BaseSettings, PostgresDsn


class APISettings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    debug: bool
    port: int = 8080

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


__all__ = [
    APISettings
]
