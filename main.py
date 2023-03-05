import os
import requests
from urllib.parse import urlparse

full_url = input("Enter the full URL of the first image: ")

parsed_url = urlparse(full_url)
site_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
folder_name = os.path.splitext(os.path.basename(parsed_url.path))[0]
file_name_format = os.path.splitext(parsed_url.path)[0] + "%d" + os.path.splitext(parsed_url.path)[1]

num_images = 4
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

for i in range(1, num_images + 1):
    file_url = site_url + file_name_format % i
    response = requests.get(file_url)
    if response.status_code == 200:
        file_name = file_name_format % i
        with open(os.path.join(folder_name, file_name), "wb") as file:
            file.write(response.content)
            print(f"{file_name} - Downloaded successfully!")
    else:
        print(f"{file_name_format % i} not found on server")
