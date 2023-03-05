import os

def create_folder(folder_name):
    """
    Create folder if it doesn't exist
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created at '{os.path.abspath(folder_name)}'")
