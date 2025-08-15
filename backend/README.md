# Backend Service

This directory contains the core backend service, built with FastAPI.

## Local Development

### Prerequisites

- Python 3.12
- A virtual environment tool (like `venv`)

### Setup and Running the Service

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Activate the virtual environment:**
    The project comes with a pre-configured virtual environment. To activate it, run:
    ```bash
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    Once the virtual environment is active, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Firebase Credentials (if needed):**
    If the service needs to connect to Firebase, follow the instructions in `INSTRUCTIONS_FIREBASE.md` to set up your `firebase-credentials.json` file in this directory.

5.  **Run the development server:**
    Use `uvicorn` to run the FastAPI application. The `--reload` flag enables auto-reloading on code changes.
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

The service will be available at `http://localhost:8000`.

### Testing

To run the automated tests, use the following command:

```bash
python3 -m unittest tests/test_tree_engine.py
```
