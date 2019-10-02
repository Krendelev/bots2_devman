import logging
import os

import requests
from dotenv import load_dotenv
from telegram import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from settings import DVMN_URL, PROXY, VERDICT


def get_task_status():
    headers = {"Authorization": f"Token {os.environ['DVMN_TOKEN']}"}
    timestamp = None
    while True:
        payload = {"timestamp": timestamp}
        try:
            response = requests.get(DVMN_URL, headers=headers, params=payload)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            continue
        response.raise_for_status()
        content = response.json()
        timestamp = (
            content.get("timestamp_to_request", None)
            or content["last_attempt_timestamp"]
        )
        if content["status"] == "found":
            for attempt in content["new_attempts"]:
                message = f"""
                    У вас проверили работу [{attempt['lesson_title']}](https://dvmn.org{attempt['lesson_url']})
                    \n{VERDICT[attempt['is_negative']]}
                """
                yield message


def start(update, context):
    try:
        status = get_task_status()
    except requests.exceptions.HTTPError as error:
        update.message.reply_text(f"Ошибка при обращении к dvmn.org – {error}")
    for msg in status:
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        filename="bot.log",
    )
    load_dotenv()

    mybot = Updater(os.environ["BOT_TOKEN"], request_kwargs=PROXY, use_context=True)

    mybot.dispatcher.add_handler(CommandHandler("start", start))

    mybot.start_polling()
    mybot.idle()
