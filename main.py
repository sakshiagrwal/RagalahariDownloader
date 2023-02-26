"""
Ragalahari Downloader
"""

import os
import os.path
import shutil
import sys
import traceback
import requests


def exists(site, path):
    """
    Check if a file exists at a given URL path.

    Args:
        site (str): The base URL of the site.
        path (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    r = requests.head(site + path)
    return r.status_code == requests.codes.ok


def check_file_exists(file_path, file_name, cycle, id_lists):
    """
    Check if a series of files exists at a given URL path.

    Args:
        file_path (str): The base URL of the site.
        file_name (str): The name of the files to check for.
        cycle (int): The number of files to check.
        id_lists (list): A list to store the IDs of the files that exist.

    Returns:
        None
    """
    i = 1
    print("Searching files...")
    while i < cycle:
        if exists(file_path, file_name % i):
            ids = file_name % i
            id_lists.append(ids)
            print("File exists: " + file_name % i)
            i += 1
        else:
            print("File not exist: " + file_name % i)
            i += 1


def create_folder(folder_name):
    """
    Create a new folder with the given name, if it does not already exist.

    Args:
        folder_name (str): The name of the folder to create.

    Returns:
        None
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def download_images(file_path, folder_name, id_lists):
    """
    Download images from the specified URL path and save them in a folder with the given name.

    Args:
        file_path (str): The URL path where the images are located.
        folder_name (str): The name of the folder to save the images in.
        id_lists (list): A list of image IDs to download.

    Returns:
        None
    """
    os.chdir(folder_name)
    for x in id_lists:
        r = requests.get(file_path + x, stream=True)
        r.raw.decode_content = True

        with open(x, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print(x + " - Saved successfully!")


def main():
    """
    Main function for downloading images from a specified URL path.

    This function prompts the user for the URL path, file name, folder name, and number of images
    to download, and then downloads the images and saves them in a folder with the specified name.

    Args:
        None

    Returns:
        Nothing
    """
    try:
        # Getting user inputs
        file_path = input("Enter the URL path of the images: ")
        file_name = input("Enter the file name: ")
        folder_name = input("Enter the folder name: ").title()
        cycle = (
            int(
                input("How many images do you want to download? (Default: 100): ")
                or 100
            )
            + 1
        )
        id_lists = []

        # Creating folder if it does not exist
        create_folder(folder_name)

        # Checking if the file exists
        check_file_exists(file_path, file_name, cycle, id_lists)

        # Downloading the images
        download_images(file_path, folder_name, id_lists)

    except KeyboardInterrupt:
        print("\nShutdown requested. Exiting...")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
