import os
from tkinter import Tk, filedialog

def rename_files():
    # Hide the main tkinter window
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    # Open a dialog to select a folder
    folder_path = filedialog.askdirectory(title="Select Folder")
    if not folder_path:
        print("No folder selected.")
        return

    # Input base name and starting number
    base_name = input("Enter the base name for files: ")
    start_number = int(input("Enter the starting number: "))

    # Get all files in the folder
    files = sorted(os.listdir(folder_path))
    file_count = len([f for f in files if os.path.isfile(os.path.join(folder_path, f))])
    digits = len(str(start_number + file_count - 1))  # Determine digit length

    # Iterate through files and rename them
    for i, file_name in enumerate(files):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_name)[1]  # Extract the file extension
            new_name = f"{base_name}{str(start_number + i).zfill(digits)}{file_extension}"
            new_path = os.path.join(folder_path, new_name)
            os.rename(file_path, new_path)

    print("Files renamed successfully!")

if __name__ == "__main__":
    rename_files()
