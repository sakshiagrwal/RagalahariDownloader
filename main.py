import os
import re
from urllib.parse import urlparse
import requests

DEFAULT_URL = "https://starzone.ragalahari.com/feb2022/hd/aakanksha-singh-clap-press-meet/aakanksha-singh-clap-press-meet1.jpg"
DEFAULT_NUM = 2
SEPARATOR = "━" * 60

full_url = input("Enter the full URL of the first image (Press enter for default): ") or DEFAULT_URL
num_images = int(input("How many images would you like to download? (Press enter for default): ") or DEFAULT_NUM)
print(SEPARATOR)

parsed_url = urlparse(full_url)
site_url = f"{parsed_url.scheme}://{parsed_url.netloc}{os.path.dirname(parsed_url.path)}/"
folder_name = re.sub(r"\d*$", "", os.path.splitext(os.path.basename(parsed_url.path))[0])
file_name = os.path.splitext(os.path.basename(full_url))[0].rstrip("1234567890")

NUM_DOWNLOADED = 0
for i in range(1, num_images + 1):
    file_name_format = file_name + str(i) + os.path.splitext(parsed_url.path)[1]
    file_path = os.path.join(folder_name, file_name_format)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print("\033[92m" + f"Folder '{folder_name}' created" + "\033[0m")
        print()

    if os.path.exists(file_path):
        print("\033[33m" + f"{file_name_format} - Already exists" + "\033[0m")
        continue

    file_url = site_url + file_name_format
    try:
        response = requests.get(file_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"\033[91m{file_name_format} - Not Found for url: {file_url}\033[0m")
        continue

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(file_path, "wb") as file:
        file.write(response.content)
    print("\033[92m" + f"{file_name_format} - Downloaded" + "\033[0m")
    NUM_DOWNLOADED += 1

if NUM_DOWNLOADED == 0:
    print()
    print("\033[91m" + "No images downloaded" + "\033[0m")
elif NUM_DOWNLOADED == num_images:
    print()
    print("\033[94m" + f"All {num_images} images downloaded at '{os.path.abspath(folder_name)}'" + "\033[0m")
else:
    print()
    print("\033[94m" + f"Downloaded {NUM_DOWNLOADED} out of {num_images} images at '{os.path.abspath(folder_name)}'" + "\033[0m")
