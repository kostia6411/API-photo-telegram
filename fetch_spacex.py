import argparse
import logging
import os

import requests

from main import IMAGES_PATH
from main import download_file


def fetch_spacex_launch(launch_namber):
    filename = 'spacex.jpeg'
    url = f"https://api.spacexdata.com/v3/launches/{launch_namber}"
    response = requests.get(url)
    response.raise_for_status()
    spacex_photo_links = response.json()["links"]["flickr_images"]
    for count, link in enumerate(spacex_photo_links):
        file_path = os.path.join(IMAGES_PATH, launch_namber, "_", count, filename)
        download_file(link, file_path)


def main():
    os.makedirs(IMAGES_PATH, exist_ok=True)
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
        fetch_spacex_launch(launch_number)
    except requests.exceptions.HTTPError:
        logging.warning("Произошла ошибка при загрузке фотографий.")



if __name__ == "__main__":
    main()
