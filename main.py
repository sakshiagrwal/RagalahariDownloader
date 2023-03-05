import os
import re
from urllib.parse import urlparse
from download_images import download_images

# get user input for URL and number of images to download
full_url = input("Enter the full URL of the first image (leave blank to use default): ")
if not full_url:
    full_url = "https://starzone.ragalahari.com/feb2020/hd/samantha-jaanu-success/samantha-jaanu-success6.jpg"
    print(f"Using default URL: {full_url}")

num_images = int(input("Enter the number of images to download: "))

# parse the URL to get the site URL, folder name, and file name format
parsed_url = urlparse(full_url)
site_url = f"{parsed_url.scheme}://{parsed_url.netloc}{os.path.dirname(parsed_url.path)}/"
folder_name = re.sub(r'\d*$', '', os.path.splitext(os.path.basename(parsed_url.path))[0])
file_name = os.path.splitext(os.path.basename(full_url))[0].rstrip("1234567890")


# download the images
download_images(site_url, folder_name, file_name, num_images, parsed_url)
