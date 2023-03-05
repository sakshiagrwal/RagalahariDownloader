# Ragalahari Downloader

This is a Python script that downloads a sequence of images from [Ragalahari](https://www.ragalahari.com/actress/starzonesearch.aspx) website. 

## Getting Started

### Prerequisites

To run this script, you'll need to have Python 3 installed on your computer, as well as the requests library. You can install requests using pip: `pip install requests`

### Usage

1. Clone this repository to your local machine. `git clone https://github.com/sakshiagrwal/ragalaharidownloader.git -b new`
2. Navigate to the directory where the script is located. `cd ragalaharidownloader`
3. Run the script by typing the following command into your terminal or command prompt: `python main.py`
4. Enter the full URL of the first image when prompted. You can also use the default [URL](https://github.com/sakshiagrwal/RagalahariDownloader/blob/edf26cc6e0f6e49ecb09896772b31bdf08a443ce/main.py#L7) by pressing Enter. [E.g.](https://starzone.ragalahari.com/feb2020/hd/samantha-jaanu-success/samantha-jaanu-success6.jpg)
5. Enter the number of images you want to download when prompted.

The script will then download the images and save them to a local directory.

### How It Works

1. The script prompts the user to enter the URL of the first image and the number of images to download.
2. It then parses the URL to extract the site URL, folder name, and file name format.
3. It loops through the range of image numbers and downloads each image using the requests library.
4. It saves each image to a file with the appropriate file name and file path.
5. It includes error checking to make sure that folders and files are not overwritten, and it prints informative messages to the console throughout the download process.
