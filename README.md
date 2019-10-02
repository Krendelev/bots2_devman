# Status checker

Check if codereview for your task is ready on [dvmn.org](https://dvmn.org/).

## How to install

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Set up Telegram bot and put its token to the `.env` file.

```bash
BOT_TOKEN=replace_with_token
```

Run `main.py`.

```bash
$ python main.py
```

Send `/start` to your bot.

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
