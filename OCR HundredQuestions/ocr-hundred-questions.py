import os
import json
import pytesseract
from PIL import Image
import re

# Specify the assets folder, cropped images folder, and output JSON file
assets_folder = "./assets"
cropped_folder = "./pictures_cut"
output_json_file = "extracted_text.json"

# Set the amount of pixels to crop from the top and bottom
CROP_TOP = 300  # Pixels to crop from the top
CROP_BOTTOM = 300  # Pixels to crop from the bottom


def crop_image(image_path, cropped_path):
    """Crops a specified number of pixels from the top and bottom of an image."""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            cropped_img = img.crop((0, CROP_TOP, width, height - CROP_BOTTOM))
            cropped_img.save(cropped_path)
    except Exception as e:
        print(f"Error cropping {image_path}: {e}")

def clean_text(text):
    """
    Cleans the text by replacing '\\n' with a space if it is surrounded by characters,
    or removing it if it isn't.
    """
    text = re.sub(r'(?<=\S)\n(?=\S)', ' ', text)
    text = text.replace('\n', '')
    return text



def extract_text_from_image(image_path, lang="eng"):
    """Extracts text from an image using OCR with a specified language."""
    try:
        with Image.open(image_path) as img:
            raw_text = pytesseract.image_to_string(img, lang=lang)
            return clean_text(raw_text)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""


def save_extracted_text_to_json(folder, output_file, lang="eng"):
    """Goes through all images in a folder, crops them, extracts text with OCR, and saves it to a JSON file."""
    data = {}

    # Ensure the cropped folder exists
    os.makedirs(cropped_folder, exist_ok=True)

    # Loop through all files in the folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        cropped_path = os.path.join(cropped_folder, filename)

        # Check if the file is an image (based on file extension)
        if os.path.isfile(file_path) and filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            # Only crop and save if the cropped file doesn't already exist
            if not os.path.exists(cropped_path):
                crop_image(file_path, cropped_path)

            # Perform OCR on the cropped image
            extracted_text = extract_text_from_image(cropped_path, lang=lang)
            data[filename] = extracted_text

    # Save the data to a JSON file
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"Data saved to {output_file}")


# Run the function
save_extracted_text_to_json(assets_folder, output_json_file, lang="deu")
