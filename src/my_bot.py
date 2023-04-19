import httpx
from loguru import logger
from telegram import Update  # type: ignore
from telegram.ext import Application
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters

from .config import MY_ID
from .config import OTHER_ID
from .config import TG_TOKEN
from .config import URL
from .create_insert import write_into_db


logger.add("main.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")


def get_ip() -> str:
    return httpx.get(URL).text


async def my_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sending report message for me
    """
    answer_to = MY_ID
    if update.message.reply_to_message:  # type: ignore
        answer_to = update.message.reply_to_message.text  # type: ignore
    if update.message.text.lower() == r"yes":  # type: ignore
        answer_ip = get_ip()
        text_send = f'"My congratulations" {answer_ip}'
        text_send_part1 = "You passed moderation from @zimkaa "
        text_send_part2 = "and this message from him"
        message_to_send = text_send_part1 + text_send_part2
        await context.bot.send_message(
            chat_id=answer_to,
            text=f"{message_to_send}\n{text_send}",
        )
    else:
        await context.bot.send_message(
            chat_id=answer_to,
            text="My master said not to say it",
        )


async def other_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sending info for OTHER_ID
    """
    name = update.effective_user
    text = update.effective_message.text  # type: ignore
    await context.bot.send_message(
        chat_id=OTHER_ID,
        text=f"Necessary info {get_ip()}",
    )
    await context.bot.send_message(
        chat_id=MY_ID,
        text=f"{name}\n{text}\n",
    )


async def ask_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sending ask
    """
    name = update.effective_user
    await update.message.reply_text(  # type: ignore
        text="I ask my master",
        reply_to_message_id=update.message.message_id,  # type: ignore
    )
    await context.bot.send_message(
        chat_id=MY_ID,
        text=f"{name}",
    )
    await context.bot.send_message(
        chat_id=MY_ID,
        text=f"{name.id}",  # type: ignore
    )


async def sending_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sending info for me
    """
    name = update.effective_user
    text = update.effective_message.text  # type: ignore
    await update.message.reply_text(  # type: ignore
        text="I don't understand you",
        reply_to_message_id=update.message.message_id,  # type: ignore
    )
    await context.bot.send_message(
        chat_id=MY_ID,
        text=f"{name}\n{text}",
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.effective_user

    m_id = update.effective_message.message_id  # type: ignore
    date = update.effective_message.date  # type: ignore
    text = update.effective_message.text  # type: ignore

    if update.effective_message.chat_id == int(MY_ID):  # type: ignore
        await my_message(update, context)
        write_into_db(name.first_name, name.is_bot, name.id, date, m_id, text, name.last_name, name.username)  # type: ignore
    elif update.effective_message.chat_id == int(OTHER_ID):  # type: ignore
        await other_message(update, context)
        write_into_db(name.first_name, name.is_bot, name.id, date, m_id, text, name.last_name, name.username)  # type: ignore
    else:
        if update.message.text == "ip":  # type: ignore
            await ask_me(update, context)
            write_into_db(name.first_name, name.is_bot, name.id, date, m_id, text, name.last_name, name.username)  # type: ignore
        else:
            await sending_info(update, context)
            write_into_db(name.first_name, name.is_bot, name.id, date, m_id, text, name.last_name, name.username)  # type: ignore


@logger.catch
def main():
    application = Application.builder().token(TG_TOKEN).build()

    application.add_handler(MessageHandler(filters.ALL, message_handler))

    application.run_polling()
