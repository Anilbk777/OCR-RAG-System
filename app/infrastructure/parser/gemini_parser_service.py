
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.messages import HumanMessage,SystemMessage
# from pathlib import Path
# import json
# from dotenv import load_dotenv
# import os
# from langchain_core.prompts import ChatPromptTemplate
# import re


# # Load environment variables
# load_dotenv()
# api_key = os.getenv("API_KEY")

# # Initialize Gemini Chat model
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )



# txt = Path(r"C:\Users\Dell\Desktop\ocr_rag_system\data\processed\Receipt_1.txt")
# content = txt.read_text(encoding="utf-8")
# # print(content)

# template = ChatPromptTemplate.from_messages([
#     ('system',"You are a helpful accountant. Output only valid JSON. Do not add any extra text or commentary."
# ),
#     ('human',"convert this {context} into a meaningful json format")
# ]
# )

# # prompt = template.invoke({'context':content})
# chain =  template | llm

# result = chain.invoke({'context':content})
# # print(result.content)

# output =result.content
# # Try to validate JSON (optional)
# # Remove anything before first { and after last } (basic cleanup)
# match = re.search(r"\{.*\}", output, re.DOTALL)
# if match:
#     clean_output = match.group(0)
#     try:
#         json_data = json.loads(clean_output)
#         with open("output.json", "w", encoding="utf-8") as f:
#             json.dump(json_data, f, indent=4, ensure_ascii=False)
#         print("✅ Clean JSON saved to output.json")
#     except json.JSONDecodeError:
#         # fallback if still invalid
#         with open("output.json", "w", encoding="utf-8") as f:
#             f.write(clean_output)
#         print("⚠️ JSON partially cleaned, saved raw to output.json")
# else:
#     # If no braces found, save raw
#     with open("output.json", "w", encoding="utf-8") as f:
#         f.write(output)
#     print("⚠️ No JSON structure detected, saved raw output")


from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import re
import json
import sys
from pathlib import Path
import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parents[3]  # go up 3 levels
sys.path.append(str(BASE_DIR))

from app.infrastructure.ocr.tesseract_service import extract_text_from_image

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Path to your image
image_path = Path(r"C:\Users\Dell\Desktop\ocr_rag_system\data\raw\Receipt_1.png")

# Get text directly from OCR (no txt file saved)
ocr_text = extract_text_from_image(image_path)

# Build prompt
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful accountant. Output only valid JSON. Do not add any extra text or commentary."),
    ("human", "Convert this {context} into a meaningful JSON format.")
])

# Run the chain
chain = template | llm
result = chain.invoke({'context': ocr_text})

# Save the JSON output
output = result.content
match = re.search(r"\{.*\}", output, re.DOTALL)
if match:
    clean_output = match.group(0)
    try:
        json_data = json.loads(clean_output)
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        print("✅ Clean JSON saved to output.json")
    except json.JSONDecodeError:
        # fallback if still invalid
        with open("output.json", "w", encoding="utf-8") as f:
            f.write(clean_output)
        print("⚠️ JSON partially cleaned, saved raw to output.json")
else:
    # If no braces found, save raw
    with open("output.json", "w", encoding="utf-8") as f:
        f.write(output)
    print("⚠️ No JSON structure detected, saved raw output")