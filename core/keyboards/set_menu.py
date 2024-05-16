from aiogram import Bot
from aiogram.types import BotCommand

from core.lexicon.lexicon_ru import LEXICON_COMMON_MENU, LEXICON_ADMIN_MENU, LEXICON_CLIENT_MENU


async def set_common_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMON_MENU.items()
    ]
    await bot.set_my_commands(main_menu_commands)

async def set_client_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_CLIENT_MENU.items()
    ]
    await bot.set_my_commands(main_menu_commands)

async def set_admin_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_ADMIN_MENU.items()
    ]
    await bot.set_my_commands(main_menu_commands)