from app.infrastructure.ocr.tesseract_service import process_images
from pathlib import Path
import os
import json
import requests
# Try to import google.generativeai, fallback to requests if not available
try:
    import langchain_google_genai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    import requests

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data/raw"
PROCESSED_DIR = BASE_DIR / "data/processed"

def call_gemini_direct(api_key, prompt):
    """Call Gemini API directly using requests"""
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def run_pipeline(api_key):
    # Step 1: Run OCR
    process_images()

    # Step 2: Prepare inputs
    inputs = []
    for txt_file in os.listdir(PROCESSED_DIR):
        if txt_file.endswith(".txt"):
            txt_path = PROCESSED_DIR / txt_file
            image_name = txt_file.replace(".txt", "")
            raw_image_path = RAW_DIR / (image_name + ".png")
            text = open(txt_path, "r", encoding="utf-8").read()
            inputs.append({"ocr_text": text, "image_file": str(raw_image_path)})

    results = []
    for item in inputs:
        prompt = f"""
        Extract structured JSON from this OCR text:
        {item['ocr_text']}
        
        Return ONLY valid JSON with fields: store_name, date, items, total_amount.
        """
        
        json_output = call_gemini_direct(api_key, prompt)
        results.append(json_output)
        print(f"✅ Processed: {item['image_file']}")
        print(f"📄 Output: {json_output}")

    return results