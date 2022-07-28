import argparse
import logging
import os
from datetime import datetime
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

from main import IMAGES_PATH
from main import download_file


def fetch_nasa_epic(api_key):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    payload = {
        "api_key": api_key
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    pictures = response.json()
    for image_nasa in pictures:
        date = image_nasa["date"]
        image = image_nasa["image"]
        disassembled_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        ready_date = disassembled_date.strftime("%Y/%m/%d")
        url_image = f"https://api.nasa.gov/EPIC/archive/natural/{ready_date}/png/{image}.png"
        file_path = os.path.join(IMAGES_PATH, image, ".png")
        download_file(url_image, file_path, params=payload)


def fetch_nasa(api_key, count):
    url = "https://api.nasa.gov/planetary/apod"
    payload = {
        "count": count,
        "api_key": api_key
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    pictures = response.json()
    for number, picture in enumerate(pictures):
        if picture.get("hdurl", False):
            picture_link = picture["hdurl"]
            extension = os.path.splitext(urlparse(picture_link).path)[1]
            file_name = f"{number}naca.{extension}"
            file_path = os.path.join(IMAGES_PATH, file_name)
            download_file(picture_link, file_path)


def main():
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    os.makedirs(IMAGES_PATH, exist_ok=True)
    parser = argparse.ArgumentParser(
        description='Скачивает картинки'
    )
    parser.add_argument('count', help='Количество фотографий', default=30, nargs="?", type=int)
    args = parser.parse_args()
    count = args.count
    try:
        fetch_nasa(api_key, count)
        fetch_nasa_epic(api_key)
    except requests.exceptions.HTTPError:
        logging.warning("Произошла ошибка при загрузке фотографий.")


if __name__ == "__main__":
    main()
