import os
import re
from urllib.parse import urlparse
import requests

# get user input for URL and number of images to download
full_url = input("Enter the full URL of the first image (leave blank to use default): ")
if not full_url:
    full_url = "https://example.com/images/image-1.jpg"  # set a default value for testing
    print(f"Using default URL: {full_url}")

num_images = int(input("Enter the number of images to download: "))

# parse the URL to get the site URL, folder name, and file name format
parsed_url = urlparse(full_url)
site_url = f"{parsed_url.scheme}://{parsed_url.netloc}{os.path.dirname(parsed_url.path)}/"
folder_name = re.sub(r'\d*$', '', os.path.splitext(os.path.basename(parsed_url.path))[0])
file_name = os.path.splitext(os.path.basename(full_url))[0].rstrip("1234567890")

# create the folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# loop through the range of image numbers
for i in range(1, num_images + 1):
    # create the file name for the current image
    file_name_format = file_name + str(i) + os.path.splitext(parsed_url.path)[1]
    # create the file path for the current image
    file_path = os.path.join(folder_name, file_name_format)

    # check if the file already exists, and skip if it does
    if os.path.exists(file_path):
        print(f"{file_name_format} already exists in {folder_name}")
        continue

    # create the URL for the current image
    file_url = site_url + file_name_format
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
