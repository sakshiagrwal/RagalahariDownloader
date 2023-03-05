import os
import requests
from urllib.parse import urlparse

full_url = input("Enter the full URL of the first image: ")
num_images = int(input("Enter the number of images to download: "))

parsed_url = urlparse(full_url)
site_url = f"{parsed_url.scheme}://{parsed_url.netloc}{os.path.dirname(parsed_url.path)}/"
folder_name = os.path.splitext(os.path.basename(parsed_url.path))[0]
file_name = os.path.splitext(os.path.basename(full_url))[0].rstrip('1234567890')

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

for i in range(1, num_images + 1):
    file_name_format = file_name + str(i) + os.path.splitext(parsed_url.path)[1]
    file_url = site_url + file_name_format
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(os.path.join(folder_name, file_name_format), "wb") as file:
            file.write(response.content)
            print(f"{file_name_format} - Downloaded successfully!")
    else:
        print(f"{file_name_format} not found on server")
