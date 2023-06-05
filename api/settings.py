from pydantic import BaseSettings, PostgresDsn


class APISettings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    debug: bool = False

    port: int = 8080

    admin_email: str = "admin@example.com"
    admin_password: str = "123"

    log_item_ttl: int = 60 * 60 * 24 * 1

    telegram_token: str | None
    telegram_users_ids: list[str] | None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


__all__ = [
    APISettings
]
