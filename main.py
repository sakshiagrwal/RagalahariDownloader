"""
Ragalahari Downloader
"""

import os
import os.path
import shutil
import sys
import requests

# Default values
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
    print("Searching for files...")

    id_list = []
    for i in range(1, num_images + 1):
        file_url = site_url + file_name_format % i
        response = requests.head(file_url, timeout=10)

        if response.status_code == requests.codes["OK"]:
            image_id = file_name_format % i
            id_list.append(image_id)
            print(f"File found: {image_id}")
        else:
            print(f"File not found: {file_name_format % i}")
            return None

    print("All files found on server")
    return id_list


def download_images(site_url, folder_name, id_list):
    """
    Downloads the specified images to the specified folder.
    """
    os.chdir(folder_name)

    print("Downloading images...")

    for image_id in id_list:
        if os.path.exists(image_id):
            print(f"{image_id} already exists, skipping...")
            continue

        file_url = site_url + image_id
        response = requests.get(file_url, stream=True, timeout=10)
        response.raw.decode_content = True

        with open(image_id, "wb") as file:
            shutil.copyfileobj(response.raw, file)

        print(f"{image_id} - Downloaded successfully!")


def main():
    """
    Main function to handle user input and download the images.
    """
    try:
        # Getting user inputs
        site_url = (
            input(
                f"Enter the URL path of the images (default: {DEFAULT_URL_PATH}): "
            ).strip()
            or DEFAULT_URL_PATH
        )
        num_images = int(
            input(
                f"How many images do you want to download? (default: {DEFAULT_NUM_IMAGES}): "
            ).strip()
            or DEFAULT_NUM_IMAGES
        )
        file_name_format = (
            input(
                f"Enter the file name format (default: {DEFAULT_FILE_NAME_FORMAT}): "
            ).strip()
            or DEFAULT_FILE_NAME_FORMAT
        )

        # Re-ask the user until valid file names are entered
        while True:
            if "%d" in file_name_format:
                id_list = check_files_exist(site_url, file_name_format, num_images)
                if id_list is not None:
                    break
                else:
                    file_name_format = input("Enter a valid file name format: ").strip()
            else:
                file_name_format = input(
                    "Invalid file name format. Please include '%d' in the format: "
                ).strip()

        # Prompt for folder name
        folder_name = (
            input(f"Enter the folder name (default: {DEFAULT_FOLDER_NAME}): ").strip()
            or DEFAULT_FOLDER_NAME
        )

        # Create folder if it does not exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Download the images
        download_images(site_url, folder_name, id_list[:num_images])

    except KeyboardInterrupt:
        print("\nShutdown requested. Exiting...")
    except requests.exceptions.Timeout:
        print("Request timed out. Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    main()
