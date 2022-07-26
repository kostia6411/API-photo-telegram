import logging
import os
import random
from time import sleep

import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    images_path = os.getenv("IMAGES_PATH", "images")
    bot_token = os.environ["TG_BOT_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]
    delay = int(os.getenv("DELAY", 14400))
    bot = telegram.Bot(token=bot_token)
    pictures = os.listdir(path=images_path)
    while True:
        random_picture = random.choice(pictures)
        try:
            with open(os.path.join(images_path, random_picture), 'rb') as photo:
                bot.send_photo(chat_id=chat_id, photo=photo)
            sleep(delay)
        except telegram.error.NetworkError:
            logging.warning("Произошла ошибка при попытке подключения к серверу телеграм, проверьте подключение у интернету.")
            sleep(30)


if __name__ == "__main__":
    main()
