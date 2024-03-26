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


@dataclass
class Settings:
    tg_bot: TgBot


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        tg_bot=TgBot(
            bot_token=env.str('TOKEN'),
            admin_id=env.int('ADMIN_ID')
        )
    )


settings = get_settings('input')
