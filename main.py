import logging
import logging.config
import os

import requests
from dotenv import load_dotenv
from telegram import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from settings import DVMN_URL, VERDICT


class TgHandler(logging.Handler):
    def __init__(self, token=None):
        logging.Handler.__init__(self)

        self.token = token
        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot
        self.chat_id = os.environ["DEV_CHAT_ID"]


def emit(self, record):
    msg = self.format(record)
    self.bot.send_message(chat_id=self.chat_id, text=msg)


def get_task_status(context):
    headers = {"Authorization": f"Token {os.environ['DVMN_TOKEN']}"}
    payload = {"timestamp": getattr(context, "timestamp", None)}

    response = requests.get(DVMN_URL, headers=headers, params=payload)
    response.raise_for_status()
    content = response.json()
    context.timestamp = (
        content.get("timestamp_to_request", None) or content["last_attempt_timestamp"]
    )
    if content["status"] == "found":
        yield from content["new_attempts"]


def compose_message(response):
    message = f"""
        У вас проверили работу [{response['lesson_title']}](https://dvmn.org{response['lesson_url']})
        \n{VERDICT[response['is_negative']]}
    """
    return message


def send_status(context):
    status = get_task_status(context)
    for result in status:
        msg = compose_message(result)
        context.bot.send_message(
            chat_id=context.job.context,
            text=msg,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


def start(update, context):
    logger.info("Bot has been started")
    context.job_queue.run_repeating(
        send_status, interval=90, first=0, context=update.message.chat_id
    )


def unknown(update, context):
    update.message.reply_text(text="Sorry, I didn't understand that command.")


def error_callback(update, context):
    logger.warning(f"Bot encountered error: {context.error}")


if __name__ == "__main__":
    load_dotenv()

    TgHandler.emit = emit
    logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
    logger = logging.getLogger()

    mybot = Updater(os.environ["TELEGRAM_TOKEN"], use_context=True)

    mybot.dispatcher.add_handler(CommandHandler("start", start))
    mybot.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    mybot.dispatcher.add_error_handler(error_callback)

    mybot.start_polling()
    mybot.idle()
