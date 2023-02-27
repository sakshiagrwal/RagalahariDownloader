"""
Ragalahari Downloader
"""

import os
import os.path
import shutil
import sys
import requests


def check_file_exists(
    site_url: str, file_name_format: str, num_images: int, id_lists: list
) -> bool:
    """
    Checks if the specified images exist on the server and returns a list of their IDs.
    """
    print("Searching for files...")

    found_files = True

    for i in range(1, num_images + 1):
        file_url = site_url + file_name_format % i
        response = requests.head(file_url, timeout=10)

        if response.status_code == requests.codes["OK"]:
            ids = file_name_format % i
            id_lists.append(ids)
            print(f"File found: {file_name_format % i}")
        else:
            print(f"File not found: {file_name_format % i}")
            found_files = False
            break  # Stop searching if the file doesn't exist

    if found_files:
        print("All files found on server")
    else:
        print("Could not find all files on server")

    return found_files


def download_images(site_url: str, folder_name: str, id_lists: list) -> None:
    """
    Downloads the specified images to the specified folder.
    """
    os.chdir(folder_name)

    print("Downloading images...")

    for image_id in id_lists:
        file_url = site_url + image_id
        response = requests.get(file_url, stream=True, timeout=10)
        response.raw.decode_content = True

        with open(image_id, "wb") as file:
            shutil.copyfileobj(response.raw, file)

        print(f"{image_id} - Downloaded successfully!")


def main() -> None:
    """
    Main function to handle user input and download the images.
    """
    try:
        # Getting user inputs
        site_url = input("Enter the URL path of the images: ")
        num_images = int(
            input("How many images do you want to download? (Default: 10): ") or 10
        )
        file_name_format = input("Enter the file name format (e.g. image-%d.jpg): ")

        # Re-ask the user until valid file names are entered
        while True:
            if "%d" in file_name_format:
                id_lists = []
                if check_file_exists(site_url, file_name_format, num_images, id_lists):
                    break
                else:
                    file_name_format = input(
                        "No files found. Enter a valid file name format: "
                    )
            else:
                file_name_format = input(
                    "Invalid file name format. Please include '%d' in the format: "
                )

        # Prompt for folder name
        folder_name = input("Enter the folder name: ")

        # Create folder if it does not exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Download the images
        download_images(site_url, folder_name, id_lists[:num_images])

    except KeyboardInterrupt:
        print("\nShutdown requested. Exiting...")
    except requests.exceptions.Timeout:
        print("Request timed out. Exiting...")
    sys.exit(1)


if __name__ == "__main__":
    main()
