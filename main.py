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
    bot_token = os.getenv("TOKEN")
    bot = telegram.Bot(token=bot_token)
    bot.send_message(chat_id="@abobus88321", text="I'm sorry Dave I'm afraid I can't do that.")
    print(bot.get_me())


if __name__ == "__main__":
    main()