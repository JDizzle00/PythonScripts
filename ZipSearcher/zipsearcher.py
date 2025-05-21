import os
import zipfile
import shutil

def search_and_copy_files(search_filename):
    assets_dir = 'assets'
    search_filename_base = os.path.splitext(search_filename)[0]
    results_dir = os.path.join('results', search_filename_base)

    found_count = 0
    total_zip_count = 0

    # Iterate through all zip files in the assets directory
    for item in os.listdir(assets_dir):
        if item.endswith('.zip'):
            total_zip_count += 1
            zip_path = os.path.join(assets_dir, item)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Iterate through all files in the zip file
                for file in zip_ref.namelist():
                    # Check if the search file exists in the zip file
                    if os.path.basename(file) == search_filename:
                        # Create results directory if it doesn't exist
                        if found_count == 0 and not os.path.exists(results_dir):
                            os.makedirs(results_dir)
                        # Extract the file to the results directory with the new name
                        new_filename = f"{os.path.splitext(item)[0]}--{search_filename}"
                        extracted_path = os.path.join(results_dir, new_filename)
                        with zip_ref.open(file) as source, open(extracted_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
                        found_count += 1
                        break  # Stop searching this zip file once the file is found

    file_or_files = "file" if found_count == 1 else "files"
    print(f"Search file found in {found_count} out of {total_zip_count} zip {file_or_files}.")

if __name__ == "__main__":
    search_filename = input("Enter the filename to search for: ")
    search_and_copy_files(search_filename)