import firebase_admin
from firebase_admin import credentials, db

# Initialize the app with service account
def initialize_firebase():
    try:
        # Method 1: Using JSON file (recommended)
        cred = credentials.Certificate("app/config/firebase-config.json")
        
        # Initialize the app with database URL
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://ocr-rag-system-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
        print("Firebase initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

