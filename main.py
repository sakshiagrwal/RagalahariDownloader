import os
import os.path
import shutil
import sys
import requests


def check_file_exists(site_url: str, file_name_format: str, num_images: int, id_lists: list) -> bool:
    print("\033[93mSearching for files...\033[0m")

    found_files = True

    for i in range(1, num_images + 1):
        file_url = site_url + file_name_format % i
        response = requests.head(file_url, timeout=10)

        if response.status_code == requests.codes["OK"]:
            ids = file_name_format % i
            id_lists.append(ids)
            print(f"\033[92mFile found:\033[0m {file_name_format % i}")
        else:
            print(f"\033[91mFile not found:\033[0m {file_name_format % i}")
            found_files = False
            break  # Stop searching if the file doesn't exist

    if found_files:
        print("\033[92mAll files found on server\033[0m")
    else:
        print("\033[91mCould not find all files on server\033[0m")

    return found_files


def download_images(site_url: str, folder_name: str, id_lists: list) -> None:
    os.chdir(folder_name)

    print("\033[93mDownloading images...\033[0m")

    for image_id in id_lists:
        if os.path.exists(image_id):
            print(f"\033[93m{image_id} already exists, skipping...\033[0m")
            continue

        file_url = site_url + image_id
        response = requests.get(file_url, stream=True, timeout=10)
        response.raw.decode_content = True

        with open(image_id, "wb") as file:
            shutil.copyfileobj(response.raw, file)

        print(f"\033[92m{image_id} - Downloaded successfully!\033[0m")


def main() -> None:
    try:
        # Getting user inputs
        site_url = input("\033[94mEnter the URL path of the images: \033[0m")
        num_images = int(input("\033[94mHow many images do you want to download? Enter 0 to download all. (Default: 10): \033[0m") or 10)
        file_name_format = input("\033[94mEnter the file name format (e.g. image-%d.jpg): \033[0m")

        # Re-ask the user until valid file names are entered
        while True:
            if "%d" in file_name_format:
                id_lists = []
                if num_images == 0 or check_file_exists(site_url, file_name_format, num_images, id_lists):
                    break
                else:
                    file_name_format = input("\033[91mEnter a valid file name format:\033[0m ")
            else:
                file_name_format = input("\033[91mInvalid file name format. Please include '%d' in the format:\033[0m ")

        # Prompt for folder name
        folder_name = input("\033[94mEnter the folder name: \033[0m")

        # Create folder if it does not exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Download the images
        if num_images == 0:
            id_lists = []
            check_file_exists(site_url, file_name_format, sys.maxsize, id_lists)
            download_images(site_url, folder_name, id_lists)
        else:
            id_lists = []
            if check_file_exists(site_url, file_name_format, num_images, id_lists):
                download_images(site_url, folder_name, id_lists[:num_images])
            else:
                print("\033[91mCould not download any files\033[0m")

    except KeyboardInterrupt:
        print("\n\033[91mShutdown requested. Exiting...\033[0m")
    except requests.exceptions.Timeout:
        print("\033[91mRequest timed out. Exiting...\033[0m")
    sys.exit(1)

if __name__ == "__main__":
    main()
