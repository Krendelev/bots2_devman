import logging
import logging.config
import os

import requests
from dotenv import load_dotenv
from telegram import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from settings import DVMN_URL, VERDICT


class TGHandler(logging.Handler):
    def __init__(self, token=None):
        logging.Handler.__init__(self)
        self.token = token

        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot
        self.chat_id = os.environ["DEV_CHAT_ID"]


def emit(self, record):
    msg = self.format(record)
    self.bot.send_message(chat_id=self.chat_id, text=msg, disable_notification=True)


def start(update, context):
    logging.info("Bot has started")
    a = 5 / 0

    c = abc()


def abc():
    b = []
    return b[2]


def error_callback(update, context):
    logging.warning(f"Bot encountered error: {context.error}")


def unknown(update, context):
    update.message.reply_text(text="Sorry, I didn't understand that command.")


if __name__ == "__main__":
    load_dotenv()

    # TGHandler.emit = emit
    # logging.config.fileConfig("logging.conf")
    # logger = logging.getLogger("loggingBot")
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", filename="bot.log"
    )

    mybot = Updater(os.environ["TELEGRAM_TOKEN"], use_context=True)

    mybot.dispatcher.add_handler(CommandHandler("start", start))
    mybot.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    mybot.dispatcher.add_error_handler(error_callback)

    mybot.start_polling()
    mybot.idle()
