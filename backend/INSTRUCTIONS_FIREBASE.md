# Firebase Setup Instructions

To enable Firebase integration for this service, you need to provide your Firebase project's service account credentials.

## Steps:

1.  **Navigate to your Firebase Project Settings:**
    *   Go to the [Firebase Console](https://console.firebase.google.com/).
    *   Select your project.
    *   Click on the gear icon (⚙️) next to "Project Overview" and select "Project settings".

2.  **Generate a new Private Key:**
    *   In the Project settings, go to the "Service accounts" tab.
    *   Click on the "Generate new private key" button.
    *   A confirmation dialog will appear. Click "Generate key".

3.  **Save the Credentials File:**
    *   A JSON file will be downloaded to your computer. This file contains your project's private credentials. **Treat this file like a password and keep it secure.**
    *   Rename this downloaded file to `firebase-credentials.json`.

4.  **Place the File in the Correct Directory:**
    *   Move the `firebase-credentials.json` file into the `core_processing_service/` directory of this project.

The `firebase_setup.py` module is designed to automatically load this file. The file is already listed in `.gitignore`, so it will not be committed to your version control history.

Once the file is in place, the application will be able to connect to your Firestore database when it starts.
