import requests
import os
import telegram
import random
from dotenv import load_dotenv
from time import sleep


IMAGES_PATH = "./images"


def download_file(url, file_path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def main():
    load_dotenv()
    bot_token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    delay = int(os.getenv("DELAY"))
    bot = telegram.Bot(token=bot_token)
    pictures = os.listdir(path='images')
    while True:
        random_pictures = random.choice(pictures)
        print(random_pictures)
        bot.send_document(chat_id=chat_id, document=open(f'images/{random_pictures}', 'rb'))
        sleep(delay)


if __name__ == "__main__":
    main()