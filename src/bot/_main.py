import logging
from typing import Optional

from telegram import BotCommand
from telegram.ext import (
    MessageHandler,
    CommandHandler,
)

from ._bot import TelegramBot, MODE


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)


def telegram_bot(
        logger: str = 'tgbot',
        mode: MODE = 'pull',
        handlers: list[MessageHandler | CommandHandler] = [],
        commands: list[BotCommand] = [],
        short_description: Optional[str] = None,
        full_description: Optional[str] = None
) -> TelegramBot:
    return TelegramBot(
        logger=logger,
        mode=mode,
        handlers=handlers,
        commands=commands,
        short_description=short_description,
        full_description=full_description
    )
