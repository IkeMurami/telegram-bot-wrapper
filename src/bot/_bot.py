import logging
from functools import partial
from typing import Literal, Optional

from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
)

from ._config import Config


async def post_init(
    application: Application,
    *,
    commands: list[BotCommand] = [],
    short_description: Optional[str] = None,
    full_description: Optional[str] = None
):

    if commands:
        await application.bot.set_my_commands(commands)

    if short_description:
        await application.bot.set_my_short_description(short_description)

    if full_description:
        await application.bot.set_my_description(full_description)


MODE = Literal['push', 'pull']


class TelegramBot:

    def __init__(
        self,
        logger: str = 'tgbot',
        mode: MODE = 'pull',
        handlers: list[MessageHandler | CommandHandler] = [],
        commands: list[BotCommand] = [],
        short_description: Optional[str] = None,
        full_description: Optional[str] = None
    ) -> None:

        self._config = Config()  # type: ignore[type-arg]
        self._mode = mode
        self._logger = logging.getLogger(logger)

        _post_init = partial(
            post_init,
            commands=commands,
            short_description=short_description,
            full_description=full_description
        )

        self._application = (
            ApplicationBuilder()
                .token(self._config.TELEGRAM_BOT_TOKEN)
                .post_init(_post_init)
                .build()
        )

        self._add_handlers(handlers)

    def _add_handlers(self, handlers: list[MessageHandler | CommandHandler]):
        for handler in handlers:
            self._application.add_handler(handler)

    # Callable[[Update, CallbackContext], None]
    def run(self):

        # self._application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        if self._mode == 'pull':
            self._application.run_polling(allowed_updates=Update.ALL_TYPES)

        if self._mode == 'push':
            self._application.run_webhook(
                listen=self._config.HOST,
                port=self._config.PORT,
                secret_token=self._config.TELEGRAM_WEBHOOK_SECRET_TOKEN,
                webhook_url=self._config.TELEGRAM_WEBHOOK_URL,
            )

        return self
