import requests
import os

site_url = input("Enter the site URL: ")
folder_name = input("Enter the folder name: ")
num_images = int(input("Enter the number of images: "))
file_name_format = input("Enter the file name format: ")

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
