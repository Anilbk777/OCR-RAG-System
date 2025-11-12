import os
from PIL import Image
import pytesseract
from pathlib import Path

# ✅ Go up 3 levels to reach project root (ocr_rag_system)
BASE_DIR = Path(__file__).resolve().parents[3]

# Define data folders relative to project root
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Make sure output folder exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

print(f"📂 Looking for images in: {RAW_DIR}")
print(f"📁 Saving text files in: {PROCESSED_DIR}")

def process_images():
    files = os.listdir(RAW_DIR)
    print(f"🧾 Found {len(files)} files: {files}")

    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = RAW_DIR / filename

            # Perform OCR
            text = pytesseract.image_to_string(Image.open(image_path))

            # Save extracted text
            txt_filename = Path(filename).stem + ".txt"
            txt_path = PROCESSED_DIR / txt_filename

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"✅ Processed: {filename} → {txt_filename}")
        else:
            print(f"⚠️ Skipped (not an image): {filename}")

if __name__ == "__main__":
    process_images()
    print("🎉 OCR processing completed! Check 'data/processed/' for .txt files.")
