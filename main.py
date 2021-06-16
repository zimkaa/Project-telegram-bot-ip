from telegram import Update  # type: ignore
from telegram.ext import CallbackContext  # type: ignore
import requests
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
import DB

from loguru import logger

import config


def message_handler(update: Update, context: CallbackContext) -> None:
    name = update.effective_user
    logger.info(name)

    logger.info(type(update.message.message_id))
    logger.info("update.message.message_id", update.message.message_id)

    m_id = update.effective_message.message_id
    date = update.effective_message.date
    text = update.effective_message.text

    if update.effective_message.chat_id == config.MY_ID:
        """
        Sending report message for me
        """
        answer_to = config.MY_ID
        if update.message.reply_to_message:
            answer_to = update.message.reply_to_message.text
        if update.message.text.lower() == r'yes':
            """
            Sending IP for user or me
            """
            answer_ip = requests.get(config.URL).text  # type: ignore
            text_send = f"\"My congratulations\" {answer_ip}"
            text_send_part1 = "You passed moderation from @zimkaa"
            text_send_part2 = "and this message from him"
            message_to_send = text_send_part1 + text_send_part2
            context.bot.send_message(
                chat_id=answer_to,
                text=f"{message_to_send}\n{text_send}",
            )
        else:
            """
            Sending message "no"
            """
            context.bot.send_message(
                chat_id=answer_to,
                text="My master said not to say it",
            )
    elif update.effective_message.chat_id == config.ABYSS_ID:
        """
        Sending info for abyss
        """
        answer_ip = requests.get(config.URL).text  # type: ignore
        context.bot.send_message(
            chat_id=config.ABYSS_ID,
            text=f"Necessary info {answer_ip}",
        )
        context.bot.send_message(
            chat_id=config.MY_ID,
            text=f"{name}\n{text}\n",
        )
        # DB.write_into_db(first_name, is_bot, telegram_id, date,
        #                  last_name=None, username=None, text=None)
        DB.write_into_db(name.first_name, name.is_bot, name.id, date,
                         m_id, name.last_name, name.username, text)
    else:
        if update.message.text == r'ip':
            """
            Sending ask
            """
            update.message.reply_text(
                text=r"I ask my master",
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
            DB.write_into_db(name.first_name, name.is_bot, name.id, date,
                             m_id, name.last_name, name.username, text)
        else:
            """
            Sending info for me
            """
            update.message.reply_text(
                text=r"I don't understand you",
                reply_to_message_id=update.message.message_id,
            )
            context.bot.send_message(
                chat_id=config.MY_ID,
                text=f"{name}\n{text}",
            )
            DB.write_into_db(name.first_name, name.is_bot, name.id, date,
                             m_id, name.last_name, name.username, text)


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
