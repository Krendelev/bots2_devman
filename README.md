# Status checker

Check if codereview for your task is ready on [dvmn.org](https://dvmn.org/).

## How to install

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Uses two bots: one for checking on Devman and other to deliver us logfiles from the first. Set up bots and put their tokens to the `.env` file. Create chat with logger bot and write down its `id`.

```bash
DVMN_TOKEN=replace_with_token
TELEGRAM_TOKEN=replace_with_token
LOGGER_TOKEN=replace_with_token
DEV_CHAT_ID=replace_with_id
```

Run `main.py`.

```bash
$ python main.py
_
```

Send `/start` to your main bot. Quit with `Ctrl-C`.

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
