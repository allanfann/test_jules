import firebase_admin
from firebase_admin import credentials, firestore
import os

# --- Firebase Initialization ---

# Construct the absolute path to the credentials file, relative to this script's location.
_current_dir = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(_current_dir, "firebase-credentials.json")

db = None

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK using the service account credentials.
    If initialization is successful, the `db` global variable will be a
    Firestore client instance.
    """
    global db
    try:
        if not firebase_admin._apps:
            # Check if the credentials file exists
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"WARNING: Firebase credentials file not found at '{CREDENTIALS_FILE}'.")
                print("Firebase features will be disabled.")
                return

            # Initialize the app with a service account
            cred = credentials.Certificate(CREDENTIALS_FILE)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("Firebase has been initialized successfully.")
        else:
            # App is already initialized
            db = firestore.client()

    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        print("Firebase features will be disabled.")

# Call initialization on module load
initialize_firebase()

def get_firestore_db():
    """
    Returns the Firestore client instance.
    Returns None if Firebase is not initialized.
    """
    if not db:
        print("Warning: Firestore client is not available. Was Firebase initialized correctly?")
    return db
