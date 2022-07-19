import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse


IMAGES_PATH = "./images"


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


def fetch_naca(api_key, pictures_link=None, namber=None):
    url = "https://api.nasa.gov/planetary/apod"
    payload = {
        "count" : "30",
        "api_key": api_key
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    pictures = response.json()
    for number, picture in enumerate(pictures):
        if picture["hdurl"]:
            picture_link = picture["hdurl"]
            extension = os.path.splitext(urlparse(picture_link).path)[1]
            file_path = f"{IMAGES_PATH}/{number}naca.{extension}"
            download_file(picture_link, file_path)


def download_file(url, file_path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    filename = 'spacex.jpeg'
    url = "https://api.spacexdata.com/v3/launches/67"
    response = requests.get(url)
    response.raise_for_status()
    spacex_photo_links = response.json()["links"]["flickr_images"]
    for count, link in enumerate(spacex_photo_links):
        file_path = f"{IMAGES_PATH}/{count}{filename}"
        download_file(link, file_path)

def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    os.makedirs(IMAGES_PATH, exist_ok=True)
    fetch_spacex_last_launch()
    fetch_naca(api_key)
    fetch_naca_epic(api_key)

if __name__ == "__main__":
    main()