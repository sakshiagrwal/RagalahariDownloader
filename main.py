"""
Ragalahari Downloader
"""

import os
import os.path
import shutil
import sys
import requests
from colorama import Fore, Style

# Default configuration
DEFAULT_URL_PATH = (
    "https://starzone.ragalahari.com/jan2019/posters/kiara-advani-vvr-interview/"
)
DEFAULT_NUM_IMAGES = 4
DEFAULT_FILE_NAME_FORMAT = "kiara-advani-vvr-interview%d.jpg"
DEFAULT_FOLDER_NAME = "kiara"


def check_files_exist(site_url, file_name_format, num_images):
    """
    Checks if the specified images exist on the server and returns a list of their IDs.
    """
    print(f"{Fore.YELLOW}Searching for files...{Style.RESET_ALL}")

    id_list = []
    for i in range(1, num_images + 1):
        file_url = site_url + file_name_format % i
        response = requests.head(file_url, timeout=10)

        if response.status_code == requests.codes["OK"]:
            image_id = file_name_format % i
            id_list.append(image_id)
            print(f"{Fore.GREEN}File found: {image_id}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}File not found: {file_name_format % i}{Style.RESET_ALL}")
            return None

    print(f"{Fore.GREEN}All files found on server{Style.RESET_ALL}")
    return id_list


def download_images(site_url, folder_name, id_list):
    """
    Downloads the specified images to the specified folder.
    """
    os.chdir(folder_name)
    current_dir = os.getcwd()

    print(f"{Fore.YELLOW}Downloading images to {current_dir}...{Style.RESET_ALL}")

    for image_id in id_list:
        if os.path.exists(image_id):
            print(f"{Fore.YELLOW}{image_id} already exists, skipping...{Style.RESET_ALL}")
            continue

        file_url = site_url + image_id
        response = requests.get(file_url, stream=True, timeout=10)
        response.raw.decode_content = True

        with open(image_id, "wb") as file:
            shutil.copyfileobj(response.raw, file)

        print(f"{Fore.GREEN}{image_id} - Downloaded successfully!{Style.RESET_ALL}")


def main():
    """
    Main function to handle user input and download the images.
    """
    try:
        # Getting user inputs
        site_url = (
            input(
                f"{Fore.YELLOW}Enter the URL path of the images {Style.RESET_ALL}(default: {DEFAULT_URL_PATH}): "
            ).strip()
            or DEFAULT_URL_PATH
        )

        while True:
            try:
                num_images = int(
                    input(
                        f"{Fore.YELLOW}How many images do you want to download?{Style.RESET_ALL} (default: {DEFAULT_NUM_IMAGES}): "
                    ).strip()
                    or DEFAULT_NUM_IMAGES
                )
                if num_images <= 0:
                    raise ValueError
                break
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a positive integer.{Style.RESET_ALL}")

        while True:
            file_name_format = (
                input(
                    f"{Fore.YELLOW}Enter the file name format{Style.RESET_ALL} (default: {DEFAULT_FILE_NAME_FORMAT}): "
                ).strip()
                or DEFAULT_FILE_NAME_FORMAT
            )
            if "%d" in file_name_format:
                id_list = check_files_exist(site_url, file_name_format, num_images)
                if id_list is not None:
                    break
                else:
                    print(
                        f"{Fore.RED}One or more files not found on server. Please enter a valid file name{Style.RESET_ALL}"
                    )
            else:
                print(f"{Fore.RED}Invalid file name format. Please include '%d' in the format.{Style.RESET_ALL}")

        folder_name = (
            input(f"{Fore.YELLOW}Enter the folder name{Style.RESET_ALL} (default: {DEFAULT_FOLDER_NAME}): ").strip()
            or DEFAULT_FOLDER_NAME
        )

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        download_images(site_url, folder_name, id_list[:num_images])
        print(f"{Fore.GREEN}Download complete!{Style.RESET_ALL}")

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Shutdown requested. Exiting...{Style.RESET_ALL}")
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}Request timed out. Exiting...{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
