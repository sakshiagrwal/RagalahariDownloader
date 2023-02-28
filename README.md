# Ragalahari Downloader

This is a simple command-line tool to download images from [Ragalahari](https://www.ragalahari.com) in bulk.

#

### Usage

1. Clone the repository:

```bash
git clone https://github.com/sakshiagrwal/RagalahariDownloader.git
```

2. Go to the downloaded repository:

```bash
cd RagalahariDownloader
```

3. Run the script:

```bash
python main.py
```

4. Follow the prompts to enter the URL path of the images, the number of images to download, the file name format, and the folder name where the images will be saved.
5. Wait for the download process to complete.

#

### Requirements

This script requires the requests module to be installed. You can install it using pip

```bash
pip install requests
```

#

### Notes

- The default number of images to download is 10, but you can specify a different number.
- The file name format should include `%d` to indicate where the image numbers go. For example, if the image files are named `image-1.jpg`, `image-2.jpg` etc. the file name format should be `image-%d.jpg`.
- If a file already exists in the target folder, the script will skip downloading that file and move on to the next file
