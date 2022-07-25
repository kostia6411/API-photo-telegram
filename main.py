import requests
import os
import telegram
from dotenv import load_dotenv


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
    bot = telegram.Bot(token=bot_token)
    bot.send_document(chat_id=chat_id, document=open('images/70_0spacex.jpeg', 'rb'))
    print(bot.get_me())


if __name__ == "__main__":
    main()