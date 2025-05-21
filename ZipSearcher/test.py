import zipfile

zip_path = 'assets/RainbowPackByBastiGHG.zip'


with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    for file in zip_ref.namelist():
        print(file)