import argparse
import logging
import os

import requests
from dotenv import load_dotenv

from tools import download_file


def fetch_spacex_launch(launch_number, images_path):
    url = f"https://api.spacexdata.com/v3/launches/{launch_number}"
    response = requests.get(url)
    response.raise_for_status()
    spacex_photo_links = response.json()["links"]["flickr_images"]
    for count, link in enumerate(spacex_photo_links):
        filename = f'{launch_number}_{count}spacex.jpeg'
        file_path = os.path.join(images_path, filename)
        download_file(link, file_path)


def main():
    load_dotenv()
    images_path = os.getenv("IMAGES_PATH", "images")
    os.makedirs(images_path, exist_ok=True)
    parser = argparse.ArgumentParser(
        description='Скачивает картинки'
    )
    parser.add_argument(
        'launch',
        help='Номер запуска',
        default=70,
        nargs="?",
        type=int
    )
    args = parser.parse_args()
    launch_number = args.launch
    try:
        fetch_spacex_launch(launch_number, images_path)
    except requests.exceptions.HTTPError as error:
        logging.warning(f"Произошла ошибка при загрузке фотографий.{error}")


if __name__ == "__main__":
    main()
