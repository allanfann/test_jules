import os
from contextlib import asynccontextmanager

import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application lifespan events for Firebase initialization.
    """
    # Startup
    print("Initializing Firebase...")
    try:
        # The credentials file is expected to be in the `backend` directory.
        # This path is relative to the `app/core` directory where this file is.
        _current_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(
            _current_dir, "..", "..", "firebase-credentials.json"
        )

        if not os.path.exists(credentials_path):
            print(
                f"WARNING: Firebase credentials file not found at '{credentials_path}'."
            )
            print("Firebase features will be disabled.")
            app.state.db = None
        else:
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred)
            app.state.db = firestore.client()
            print("Firebase has been initialized successfully.")

    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        app.state.db = None

    yield

    # Shutdown
    print("Firebase shutdown.")
    # No explicit shutdown needed for firebase-admin


def get_firestore_db(request: Request) -> firestore.Client:
    """
    FastAPI dependency to get the Firestore client from the app state.
    """
    if not hasattr(request.app.state, "db") or request.app.state.db is None:
        raise HTTPException(
            status_code=503,
            detail="Firebase service is not available. Check server logs for initialization errors.",
        )
    return request.app.state.db
