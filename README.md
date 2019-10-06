[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5700d2d4ac25487f927e8bc5a00ac113)](https://www.codacy.com/manual/Krendelev/bots1_devman?utm_source=github.com&utm_medium=referral&utm_content=Krendelev/bots1_devman&utm_campaign=Badge_Grade)

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
TELEGRAM_TOKEN=replace_with_token
```

Run `main.py`.

```bash
$ python main.py
_
```

Send `/start` to your bot.

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
