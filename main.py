import os
import os.path
import shutil
import sys
import traceback
import requests


def exists(site, path):
    r = requests.head(site + path)
    return r.status_code == requests.codes.ok


def check_file_exists(file_path, file_name, cycle, id_lists):
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
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def download_images(file_path, folder_name, id_lists):
    os.chdir(folder_name)
    for x in id_lists:
        r = requests.get(file_path + x, stream=True)
        r.raw.decode_content = True

        with open(x, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print(x + " - Saved successfully!")


def main():
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
