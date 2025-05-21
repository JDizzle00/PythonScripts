import os
import json
import pytesseract
from PIL import Image, ImageStat

# Specify the assets folder and output JSON file
assets_folder = "./assets"
output_json_file = "extracted_text.json"

def extract_text_from_image(image_path, lang="eng"):
    """Extracts text from an image using OCR with a specified language."""
    try:
        with Image.open(image_path) as img:
            return pytesseract.image_to_string(img, lang=lang)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""

def get_background_color(image_path):
    """Determines the background color of an image by averaging its pixel values and classifies it."""
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")  # Ensure image is in RGB mode
            stat = ImageStat.Stat(img)
            avg_color = tuple(map(int, stat.mean))  # Average color as (R, G, B)
            
            # Classify the background color based on the average RGB value
            if avg_color[0] > avg_color[1] and avg_color[0] > avg_color[2]:
                return "red"
            elif avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]:
                return "green"
            elif avg_color[2] > avg_color[0] and avg_color[2] > avg_color[1]:
                return "blue"
            else:
                return "yellow"
    except Exception as e:
        print(f"Error determining background color for {image_path}: {e}")
        return None

def process_extracted_text(text):
    """Checks for specific keywords at the start of the text and returns a category and the modified text."""
    keywords = ["SPIEL", "VIRUS", "HÖCHSTSTRAFE"]
    for keyword in keywords:
        if text.upper().startswith(keyword):
            category = keyword.lower()
            text = text[len(keyword):].strip()  # Remove the keyword and any leading/trailing whitespace
            return category, text
    return None, text

def save_extracted_text_to_json(folder, output_file, lang="eng"):
    """Goes through all images in a folder, extracts text with OCR, determines background color, and saves it in a JSON file."""
    data = {}

    # Loop through all files in the folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        
        # Check if the file is an image (based on file extension)
        if os.path.isfile(file_path) and filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            extracted_text = extract_text_from_image(file_path, lang=lang)
            category, modified_text = process_extracted_text(extracted_text)
            background_color = get_background_color(file_path)
            
            data[filename] = {
                "text": modified_text,
                "background_color": background_color
            }
            
            if category:
                data[filename]["category"] = category

    # Save the data to a JSON file
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"Data saved to {output_file}")

# Run the function
save_extracted_text_to_json(assets_folder, output_json_file, lang="deu")
