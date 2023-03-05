import os
import requests

def download_images(site_url, folder_name, file_name, num_images, parsed_url):
    """
    Download images from a given URL
    """
    # check if the folder exists and has any files before downloading images
    folder_path = os.path.abspath(folder_name)
    if os.path.exists(folder_path) and os.listdir(folder_path):
        print(f"Skipping folder creation as '{folder_name}' already exists and has files.")
    else:
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created at '{folder_path}'")

    # loop through the images and download them
    for index, _ in enumerate(range(1, num_images + 1), start=1):
        # create the file name for the current image
        file_name_format = f"{file_name}{index}{os.path.splitext(parsed_url.path)[1]}"
        # create the file path for the current image
        file_path = os.path.join(folder_name, file_name_format)

        try:
            # check if the file already exists, and skip if it does
            if os.path.exists(file_path):
                print(f"{file_name_format} already exists in {folder_name}")
                continue

            # create the URL for the current image
            file_url = f"{site_url}{file_name_format}"
            # download the image from the URL with a 10-second timeout
            response = requests.get(file_url, timeout=10)

            # check if the image was downloaded successfully, and save it to the file path if it was
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
                    print(f"{file_name_format} - Downloaded successfully!")
            # print an error message if the image was not found on the server
            else:
                print(f"{file_name_format} not found on server")
        except requests.exceptions.RequestException as error:
            print(f"Error downloading {file_name_format}: {error}")
