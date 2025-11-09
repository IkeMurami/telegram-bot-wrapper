from ikemurami.telegram import telegram_bot
import logging
import random
import pytz
from datetime import datetime, time

from functools import wraps

from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationHandlerStop,
    TypeHandler,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
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


async def send_scheduled_message(context: ContextTypes.DEFAULT_TYPE):
    """Send a random message to all subscribed users."""
    MESSAGES = [
        'Hi, giraffe!',
        'Hi, begemoth!'
    ]
    random_message = random.choice(MESSAGES)
    # Send to all users
    for user_id in list(USERS): 
        try:
            await context.bot.send_message(chat_id=user_id, text=random_message)
            print(f'Scheduled message sent to {user_id}')
        except Exception as e:
            print(f'Failed to send message to {user_id}: {e}')
            # Optionally remove users that can't be reached
            # USERS.remove(user_id)


def scheduled_time():
    # Schedule for 2:00 AM Moscow time every day (the function will check if it's Thursday)
    moscow_time = pytz.timezone('Europe/Moscow')

    # Convert 2:00 AM Moscow time to UTC for scheduling
    # First create a full datetime object in Moscow time zone
    now = datetime.now(moscow_time)
    target_datetime = moscow_time.localize(
        datetime.combine(now.date(), time(hour=2, minute=20))
    )
    # Convert to UTC time for the scheduler
    target_time_utc = target_datetime.astimezone(pytz.UTC).time()

    return target_time_utc


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
        .daily_job(
            send_scheduled_message,
            scheduled_time()
        )
        .run()
    )


if __name__ == '__main__':
    main()
