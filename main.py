import logging
import os
import time

import requests
from dotenv import load_dotenv
from telegram import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from settings import DVMN_URL, VERDICT


class TGHandler(logging.Handler):
    def __init__(self, token):
        logging.Handler.__init__(self)
        self.token = token

        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot
        # self.dispatcher.add_handler(CommandHandler("start", emit))


def emit(self, record):
    msg = self.format(record)
    self.bot.send_message(chat_id=149258025, text=msg, disable_notification=True)
    # self.bot.message.reply_text(msg, disable_notification=True)


def start(update, context):
    try:
        a = 5 / 0
    except ZeroDivisionError as e:
        logger.error(e)

    c = abc()


def abc():
    b = [0]
    return b[2]


def error_callback(update, context):
    logger.warning(f"{update.message.text} caused error {context.error}")


def unknown(update, context):
    update.message.reply_text(text="Sorry, I didn't understand that command.")


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        datefmt="%d-%b-%y %H:%M:%S",
        # filename="bot.log",
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    TGHandler.emit = emit
    logger.addHandler(TGHandler(os.environ["LOGGER_TOKEN"]))

    mybot = Updater(os.environ["TELEGRAM_TOKEN"], use_context=True)

    mybot.dispatcher.add_handler(CommandHandler("start", start))
    mybot.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    mybot.dispatcher.add_error_handler(error_callback)

    mybot.start_polling()
    mybot.idle()
