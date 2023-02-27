"""
Ragalahari Downloader
"""

import os
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

# Input URL
url = input("Enter the url of the page you want to download images from: ")

# Create a session object
session = requests.Session()

# Make a request to the URL using the session object
response = session.get(url)

# Parse the HTML content using html5lib parser
soup = BeautifulSoup(response.content, "html5lib")

# Find all the links that point to images
image_links = []
for a in soup.find_all("a"):
    if a.find("img"):
        href = a.get("href")
        if href.endswith(".aspx"):
            image_links.append(urljoin(url, href))

# Create a folder to store the images
folder_name = os.path.basename(url).replace(".aspx", "")
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Download all the images using a thread pool
def download_image(img_url):
    """Download an image from a URL and save it to a folder.

    Args:
        img_url (Any): The URL of the image to download.

    Returns:
        None: This function doesn't return anything, but it saves the downloaded image to a folder.

    Raises:
        Exception: If there's an error downloading or saving the image.
    """
    try:
        # Get the filename of the image
        filename = os.path.basename(img_url).replace(".aspx", ".jpg")

        # Check if the image has already been downloaded
        filepath = os.path.join(folder_name, filename)
        if os.path.exists(filepath):
            print(f"{filename} already exists")
            return

        # Check if the folder name is in the image URL
        if folder_name in img_url:
            # Download the image
            img_response = session.get(img_url)

            # Parse the HTML content to get the actual image URL
            img_soup = BeautifulSoup(img_response.content, "html.parser")
            img_tag = img_soup.find("img", {"data-srcset": True})
            if img_tag:
                actual_img_url = (
                    img_tag["data-srcset"]
                    .split(",")[-1]
                    .split(" ")[0]
                    .replace(
                        "https://szcdn.ragalahari.com",
                        "https://starzone.ragalahari.com",
                    )
                )

                # Save the image to the folder
                with open(filepath, "wb") as handler:
                    handler.write(session.get(actual_img_url).content)

                print(f"Downloaded {filename} from '{actual_img_url}'")
            else:
                print(f"No image found at {img_url}")
        else:
            return
    except requests.exceptions.RequestException as err:
        print(f"Error downloading {img_url}: {err}")


with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(download_image, image_links)
