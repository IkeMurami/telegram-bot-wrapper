from ikemurami.telegram import telegram_bot
import logging

from telegram import Update
from telegram.ext import (
    ApplicationHandlerStop,
    TypeHandler,
    MessageHandler,
    filters
)


logger = logging.getLogger('tgbot')


async def is_admin(update, context):
    ADMINS = []
    user_id = update.message.from_user.id
    logger.info(f'Checking admin permissions for telegram user id: {user_id}')
    if user_id not in ADMINS:
        raise ApplicationHandlerStop


async def handle_message(update, context):
    """Handle user messages and respond them."""
    if not update.message or not update.message.from_user:
        return

    user_message = update.message.text
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username  # or update.message.from_user.first_name

    # Get the current model for this user
    logger.info(f'({context.bot.username}) Received message from {user_name} ({user_id}): {user_message}')

    if not user_message:
        return

    try:
        await update.message.reply_text('process your request...')
    except Exception as e:
        logger.error(f'Error generating response: {e}')
        await update.message.reply_text('something wrong')


async def echo_handler(update, context):
    """Echo the received message."""
    if update.message:
        await update.message.reply_text(update.message.text)


def main():
    _ = (
        telegram_bot(
            logger='bot-core',
            mode='pull',
            handlers=[
                # Проверяем, что пользователь admin
                TypeHandler(Update, is_admin), # type: ignore

                # Отвечаем на ответы и на призывы
                MessageHandler(filters.TEXT & (filters.Entity('mention') | filters.REPLY), handle_message),
                # Отвечаем на все, кроме команд
                MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler),
            ],
            short_description='Test bot',
            # full_description='Telegram bot by IkeMurami',
        )
        .run()
    )


if __name__ == '__main__':
    main()
