import requests
from main import IMAGES_PATH
from datetime import datetime
from urllib.parse import urlparse
from main import download_file
import os
from dotenv import load_dotenv
import argparse


def fetch_naca_epic(api_key):
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
        file_path = f"{IMAGES_PATH}/{image}.png"
        download_file(url_image, file_path, params=payload)


def fetch_naca(api_key,count):
    url = "https://api.nasa.gov/planetary/apod"
    payload = {
        "count" : count,
        "api_key": api_key
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    pictures = response.json()
    for number, picture in enumerate(pictures):
        if picture.get("hdurl", False):
            picture_link = picture["hdurl"]
            extension = os.path.splitext(urlparse(picture_link).path)[1]
            file_path = f"{IMAGES_PATH}/{number}naca.{extension}"
            download_file(picture_link, file_path)

def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    os.makedirs(IMAGES_PATH, exist_ok=True)
    fetch_naca(api_key)
    fetch_naca_epic(api_key)
    parser = argparse.ArgumentParser(
        description='Скачивает картинки'
    )
    parser.add_argument('count', help='Количество фотографий', default=30, nargs="?", type=int)
    args = parser.parse_args()
    count = args.count

if __name__ == "__main__":
    main()
