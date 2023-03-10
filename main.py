import os
import re
import time
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
TOTAL_SIZE = 0
start_time = time.time()
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
        response = requests.get(file_url, stream=True, timeout=10)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length"))
        TOTAL_SIZE += total_size
    except requests.exceptions.RequestException as e:
        print(f"\033[91m{file_name_format} - Not Found for url: {file_url}\033[0m")
        continue

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    downloaded_size = 0
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
                downloaded_percentage = int(downloaded_size / total_size * 100)
                elapsed_time = time.time() - start_time
                download_speed = downloaded_size / elapsed_time
                print(
                    f"\r\033[92m{file_name_format} - Downloaded {downloaded_percentage}% - {download_speed/1024:.2f} KB/s\033[0m",
                    end="")
    print()
    NUM_DOWNLOADED += 1

if NUM_DOWNLOADED == 0:
    print()
    print("\033[91m" + "No images downloaded" + "\033[0m")
elif NUM_DOWNLOADED == num_images:
    print()
    print("\033[94m" + f"All {num_images} images downloaded at '{os.path.abspath(folder_name)}' - Total size: {TOTAL_SIZE/1024/1024:.2f} MB" + "\033[0m")
else:
    print()
    print("\033[94m" + f"Downloaded {NUM_DOWNLOADED} out of {num_images} images at '{os.path.abspath(folder_name)}'" + "\033[0m")
