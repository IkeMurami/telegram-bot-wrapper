from ikemurami.telegram import telegram_bot
import logging

from functools import wraps

from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationHandlerStop,
    TypeHandler,
    MessageHandler,
    CommandHandler,
    filters
)


ADMINS = [
    394898882,
]
USERS = set()


logger = logging.getLogger('tgbot')


def admin_check(func):
    @wraps(func)
    async def wrapper(update: Update, context):
        user_id = update.effective_user.id if update.effective_user else None
        if user_id not in ADMINS:
            logger.warning(f'Unauthorized access denied for user {user_id}.')
            return
        return await func(update, context)
    return wrapper


@admin_check
async def hello_handler(update, context):
    """Handle the /hello command."""
    # Add user to subscribers list
    if not update.effective_user:
        return

    user_id = update.effective_user.id
    USERS.add(user_id)
    if update.message:
        await update.message.reply_text(f'Hello, {user_id}! I am your bot. How can I assist you today?')


@admin_check
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


@admin_check
async def echo_handler(update, context):
    """Echo the received message."""
    if update.message:
        await update.message.reply_text(update.message.text)


def main():
    _ = (
        telegram_bot(
            logger='bot-core',
            mode='pull',
            commands=[
                BotCommand('hello', 'Hello from bot'),
            ],
            handlers=[
                # Command handlers
                CommandHandler('hello', hello_handler),  # /hello

                # Отвечаем на ответы и на призывы
                MessageHandler(filters.TEXT & ~filters.COMMAND & (filters.Entity('mention') | filters.REPLY), handle_message),
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
