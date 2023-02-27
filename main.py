import os
import os.path
import shutil
import requests
import tkinter as tk
from tkinter import messagebox

def exists(site, path):
    r = requests.head(site + path)
    return r.status_code == requests.codes.ok


def check_file_exists(file_path, file_name, cycle, id_lists):
    i = 1
    while i < cycle:
        if exists(file_path, file_name % i):
            ids = file_name % i
            id_lists.append(ids)
            i += 1
        else:
            i += 1
    return len(id_lists) > 0


def download_images(file_path, folder_name, id_lists):
    os.chdir(folder_name)
    for x in id_lists:
        r = requests.get(file_path + x, stream=True)
        r.raw.decode_content = True

        with open(x, "wb") as f:
            shutil.copyfileobj(r.raw, f)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Downloader")

        # Create widgets
        self.file_path_label = tk.Label(self, text="URL path:")
        self.file_path_entry = tk.Entry(self)
        self.file_name_label = tk.Label(self, text="File name:")
        self.file_name_entry = tk.Entry(self)
        self.folder_name_label = tk.Label(self, text="Folder name:")
        self.folder_name_entry = tk.Entry(self)
        self.cycle_label = tk.Label(self, text="Number of images:")
        self.cycle_entry = tk.Entry(self)
        self.download_button = tk.Button(self, text="Download", command=self.download)

        # Pack widgets
        self.file_path_label.pack()
        self.file_path_entry.pack()
        self.file_name_label.pack()
        self.file_name_entry.pack()
        self.folder_name_label.pack()
        self.folder_name_entry.pack()
        self.cycle_label.pack()
        self.cycle_entry.pack()
        self.download_button.pack()

    def download(self):
        try:
            # Get input values
            file_path = self.file_path_entry.get()
            file_name = self.file_name_entry.get()
            folder_name = self.folder_name_entry.get().title()
            cycle = int(self.cycle_entry.get() or 100) + 1
            id_lists = []

            # Check if files exist
            if check_file_exists(file_path, file_name, cycle, id_lists):
                # Create folder if it doesn't exist
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                # Download images
                download_images(file_path, folder_name, id_lists)

                # Show success message
                messagebox.showinfo("Success", "Images downloaded successfully!")
            else:
                messagebox.showerror("Error", "No files found for download.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()
