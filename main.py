"""
Ragalahari Downloader
"""

import os
import os.path
import shutil
import sys
import requests


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
                "Enter the URL path of the images (default: https://starzone.ragalahari.com/jan2019/posters/kiara-advani-vvr-interview/): "
            ).strip()
            or "https://starzone.ragalahari.com/jan2019/posters/kiara-advani-vvr-interview/"
        )
        num_images = int(
            input("How many images do you want to download? (default: 4): ").strip()
            or 4
        )
        file_name_format = (
            input(
                "Enter the file name format (default: kiara-advani-vvr-interview%d.jpg): "
            ).strip()
            or "kiara-advani-vvr-interview%d.jpg"
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
            input("Enter the folder name (default: images/): ").strip() or "images/"
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
