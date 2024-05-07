from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    bot_token: str
    admin_id: int


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str
    db_port: int


@dataclass
class Settings:
    tg_bot: TgBot
    db_postgres: DatabaseConfig


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        tg_bot=TgBot(
            bot_token=env.str('TOKEN'),
            admin_id=env.int('ADMIN_ID')
        ),
        db_postgres=DatabaseConfig(
            database=env.str('DB_NAME'),
            db_user=env.str('DB_USER'),
            db_password=env.str('DB_PASSWORD'),
            db_host=env.str('DB_HOST'),
            db_port=env.int('DB_PORT')
        )
    )


settings = get_settings('.env')
