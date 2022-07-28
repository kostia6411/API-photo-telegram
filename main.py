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
    pictures = os.listdir(path='images')
    while True:
        random_pictures = random.choice(pictures)
        print(random_pictures)
        bot.send_photo(chat_id=chat_id, photo=open(
            os.path.join("images", random_pictures),
            'rb'
        ))
        sleep(delay)


if __name__ == "__main__":
    main()
