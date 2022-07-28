import logging
import os
import random
from time import sleep

import requests
import telegram
from dotenv import load_dotenv


IMAGES_PATH = os.path.join(".", "images")


def download_file(url, file_path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def main():
    load_dotenv()
    bot_token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    delay = int(os.getenv("DELAY", 14400))
    bot = telegram.Bot(token=bot_token)
    pictures = os.listdir(path=IMAGES_PATH)
    while True:
        random_picture = random.choice(pictures)
        try:
            with open(os.path.join(IMAGES_PATH, random_picture), 'rb') as photo:
                bot.send_photo(chat_id=chat_id, photo=photo)
        except telegram.error:
            logging.warning("Произошла ошибка связанная с телеграм.")
        sleep(delay)


if __name__ == "__main__":
    main()
