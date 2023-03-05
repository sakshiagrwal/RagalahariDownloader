import requests
import os

site_url = "https://starzone.ragalahari.com/jan2019/posters/kiara-advani-vvr-interview/"
folder_name = "kiara"
num_images = 4
file_name_format = "kiara-advani-vvr-interview%d.jpg"

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
