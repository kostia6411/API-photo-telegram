import requests
import os


IMAGES_PATH = "./images"


def download_file(url, file_path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def main():
    pass


if __name__ == "__main__":
    main()