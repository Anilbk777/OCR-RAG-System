# # from app.infrastructure.ocr.tesseract_service import process_images
# from langchain_google_genai import ChatGoogleGenerativeAI
# import base64
# from langchain.messages import HumanMessage
# from dotenv import load_dotenv
# import os
# from pathlib import Path
# from langchain.output_parsers import JsonOutputParser

#     # Load environment variables from .env file
# load_dotenv()

#     # Access the variables
# api_key = os.getenv("API_KEY")

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
    
# )


# image_file_path = Path("C:/Users/Dell/Desktop/ocr_rag_system/data/raw/Receipt_1.png")


# # Example using a local image file encoded in base64


# with open(image_file_path, "rb") as image_file:
#     encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# message_local = HumanMessage(
#     content=[
#         {"type": "text", "text": "Describe the local image."},
#         {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image}"},
#     ]
# )
# result_local = llm.invoke([message_local])
# print(f"Response for local image: {result_local.content}")


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage
from langchain_core.output_parsers import StructuredOutputParser, ResponseSchema
import base64
from pathlib import Path
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize Gemini Chat model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Encode image as base64
image_file_path = Path("C:/Users/Dell/Desktop/ocr_rag_system/data/raw/Receipt_1.png")
with open(image_file_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# Define JSON schema you want from the model
response_schemas = [
    ResponseSchema(name="date", description="The date of the receipt or invoice"),
    ResponseSchema(name="total_amount", description="Total amount in the receipt"),
    ResponseSchema(name="vendor_name", description="Vendor or store name"),
    ResponseSchema(name="items", description="List of items with name and price")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# Build prompt with proper format instructions
prompt = f"""
Analyze this receipt image and extract the following information:

- date: The date of the receipt or invoice
- total_amount: Total amount in the receipt  
- vendor_name: Vendor or store name
- items: List of items with name and price

Return the data in JSON format.

Format instructions:
{format_instructions}
"""

# Create message with image
message_local = HumanMessage(
    content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image}"},
    ]
)

# Invoke Gemini
response = llm.invoke([message_local])

# Parse JSON output
try:
    parsed = output_parser.parse(response.content)
    print("✅ Successfully parsed structured data:")
    print(json.dumps(parsed, indent=4))
except Exception as e:
    print("❌ Failed to parse JSON:")
    print(f"Error: {e}")
    print(f"Raw output: {response.content}")