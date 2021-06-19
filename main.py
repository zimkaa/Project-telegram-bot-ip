from telegram import Update  # type: ignore
from telegram.ext import CallbackContext  # type: ignore
import requests
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters

from loguru import logger

from CreateInsert import write_into_db
import config


logger.add("main.log", format="{time} {level} {message}", level="DEBUG",
           rotation="10 MB", compression="zip")


def get_ip() -> str:
    return requests.get(config.URL).text  # type: ignore


def my_message(update: Update, context: CallbackContext) -> None:
    """
    Sending report message for me
    """
    answer_to = config.MY_ID
    if update.message.reply_to_message:
        answer_to = update.message.reply_to_message.text
    if update.message.text.lower() == r"yes":
        """
        Sending IP for user or me
        """
        answer_ip = get_ip()
        text_send = f"\"My congratulations\" {answer_ip}"
        text_send_part1 = "You passed moderation from @zimkaa "
        text_send_part2 = "and this message from him"
        message_to_send = text_send_part1 + text_send_part2
        context.bot.send_message(
            chat_id=answer_to,
            text=f"{message_to_send}\n{text_send}",
        )
    else:
        """
        Sending message "No"
        """
        context.bot.send_message(
            chat_id=answer_to,
            text="My master said not to say it",
        )


def other_message(update: Update, context: CallbackContext) -> None:
    """
    Sending info for OTHER_ID
    """
    name = update.effective_user
    text = update.effective_message.text
    context.bot.send_message(
        chat_id=config.OTHER_ID,
        text=f"Necessary info {get_ip()}",
    )
    context.bot.send_message(
        chat_id=config.MY_ID,
        text=f"{name}\n{text}\n",
    )


def ask_me(update: Update, context: CallbackContext) -> None:
    """
    Sending ask
    """
    name = update.effective_user
    update.message.reply_text(
        text="I ask my master",
        reply_to_message_id=update.message.message_id,
    )
    context.bot.send_message(
        chat_id=config.MY_ID,
        text=f"{name}",
    )
    context.bot.send_message(
        chat_id=config.MY_ID,
        text=f"{name.id}",
    )


def sending_info(update: Update, context: CallbackContext) -> None:
    """
    Sending info for me
    """
    name = update.effective_user
    text = update.effective_message.text
    update.message.reply_text(
        text="I don't understand you",
        reply_to_message_id=update.message.message_id,
    )
    context.bot.send_message(
        chat_id=config.MY_ID,
        text=f"{name}\n{text}",
    )


def message_handler(update: Update, context: CallbackContext) -> None:
    name = update.effective_user

    m_id = update.effective_message.message_id
    date = update.effective_message.date
    text = update.effective_message.text

    if update.effective_message.chat_id == config.MY_ID:
        my_message(update, context)
        write_into_db(name.first_name, name.is_bot, name.id, date,
                         m_id, text, name.last_name, name.username)
    elif update.effective_message.chat_id == config.OTHER_ID:
        other_message(update, context)
        write_into_db(name.first_name, name.is_bot, name.id, date,
                         m_id, text, name.last_name, name.username)
    else:
        if update.message.text == "ip":
            ask_me(update, context)
            write_into_db(name.first_name, name.is_bot, name.id, date,
                             m_id, text, name.last_name, name.username)
        else:
            sending_info(update, context)
            write_into_db(name.first_name, name.is_bot, name.id, date,
                             m_id, text, name.last_name, name.username)


@logger.catch
def main():
    updater = Updater(
        token=config.TG_TOKEN,
        use_context=True,
    )

    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.all, message_handler))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
