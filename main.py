import logging
import os
import json
import requests
from dotenv import load_dotenv
from telegram import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from settings import DVMN_URL, PROXY, VERDICT


def get_task_status():
    # headers = {"Authorization": f"Token {os.environ['DVMN_TOKEN']}"}
    # timestamp = None
    # while True:
    #     payload = {"timestamp": timestamp}
    #     try:
    #         response = requests.get(DVMN_URL, headers=headers, params=payload)
    #     except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
    #         continue
    #     response.raise_for_status()
    #     content = response.json()
    #     timestamp = (
    #         content.get("timestamp_to_request", None)
    #         or content["last_attempt_timestamp"]
    #     )
    with open("_workfiles/out.json") as fh:
        content = json.load(fh)
        if content["status"] == "found":
            yield content["new_attempts"]


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
        print(status)
        msg = compose_message(task)
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
