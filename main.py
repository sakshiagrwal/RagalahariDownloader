import requests
from bs4 import BeautifulSoup
import os

url = input("Enter the url of the page you want to download images from: ")

# Create a session object
session = requests.Session()

# Make a request to the URL using the session object
response = session.get(url)

# Parse the HTML content using lxml parser
soup = BeautifulSoup(response.content, "lxml")

# Find all the links that point to images
image_links = []
for a in soup.find_all("a"):
    if a.find("img"):
        href = a.get("href")
        if href.endswith(".aspx"):
            image_links.append("https://www.ragalahari.com" + href)

# Create a folder to store the images
folder_name = url.split("/")[-1].replace(".aspx", "")
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Download all the images
for img_url in image_links:
    try:
        # Get the filename of the image
        filename = img_url.split("/")[-1].replace(".aspx", ".jpg")

        # Download the image
        response = session.get(img_url)

        # Parse the HTML content to get the actual image URL
        soup = BeautifulSoup(response.content, "lxml")
        img_tag = soup.find("img", {"data-srcset": True})
        if img_tag:
            actual_img_url = (
                img_tag["data-srcset"]
                .split(",")[-1]
                .split(" ")[0]
                .replace(
                    "https://szcdn.ragalahari.com", "https://starzone.ragalahari.com"
                )
            )
            # Print the actual image URL for debugging
            print(actual_img_url)

            # Save the image to the folder
            filepath = os.path.join(folder_name, filename)
            with open(filepath, "wb") as handler:
                handler.write(session.get(actual_img_url).content)

            print(f"Downloaded {filename}")
        else:
            print(f"No image found at {img_url}")
            print(soup)
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")
