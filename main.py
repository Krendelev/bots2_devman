import argparse
import logging
import os

import requests
from dotenv import load_dotenv
from telegram import ParseMode
from telegram.ext import CommandHandler, Updater

from settings import DVMN_URL, VERDICT


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
            yield from content["new_attempts"]


def compose_message(response):
    message = f"""
        У вас проверили работу [{response['lesson_title']}](https://dvmn.org{response['lesson_url']})
        \n{VERDICT[response['is_negative']]}
    """
    return message


def start(update, context):
    try:
        status = get_task_status()
    except requests.exceptions.HTTPError as error:
        update.message.reply_text(f"Ошибка при обращении к dvmn.org – {error}")
    for task in status:
        msg = compose_message(task)
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


def get_proxy():
    parser = argparse.ArgumentParser(description="Telegram bot to check on devman.org")
    parser.add_argument("URL", nargs="?", help="Proxy URL")
    return {"proxy_url": parser.parse_args().URL}


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        filename="bot.log",
    )
    load_dotenv()

    proxy = get_proxy()
    mybot = Updater(
        os.environ["TELEGRAM_TOKEN"], request_kwargs=proxy, use_context=True
    )

    mybot.dispatcher.add_handler(CommandHandler("start", start))

    mybot.start_polling()
    mybot.idle()
