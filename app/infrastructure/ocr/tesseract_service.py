from PIL import Image
import pytesseract
from pathlib import Path

def extract_text_from_image(image_path: Path) -> str:
    """
    Takes an image path and returns the extracted text as a string.
    """
    text = pytesseract.image_to_string(Image.open(image_path))
    return text


def extract_text_from_folder(folder_path: Path) -> dict:
    """
    Takes a folder path, performs OCR on all image files, 
    and returns a dictionary {filename: text}.
    """
    results = {}
    for file in folder_path.iterdir():
        if file.suffix.lower() in ('.png', '.jpg', '.jpeg', '.bmp', '.tiff'):
            text = extract_text_from_image(file)
            results[file.name] = text
    return results
