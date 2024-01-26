from functools import lru_cache

import psycopg
from psycopg_pool import ConnectionPool
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

conninfo = (
    f"user={settings.db_user} password={settings.db_password}"
    f" host={settings.db_host} port={settings.db_port} dbname={settings.db_name}"
)


def get_conn():
    return psycopg.connect(conninfo=conninfo)


@lru_cache()
def get_pool():
    return ConnectionPool(conninfo=conninfo)


# uncomment to see psycopg.pool logs
# import logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
# logging.getLogger("psycopg.pool").setLevel(logging.INFO)
