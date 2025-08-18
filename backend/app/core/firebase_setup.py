import os
from contextlib import asynccontextmanager

import firebase_admin
import torch
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException, Request
from transformers import BertModel, BertTokenizer


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application lifespan events for Firebase and BERT model initialization.
    """
    # --- Firebase Startup ---
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

    # --- BERT Model Startup ---
    print("Loading BERT model...")
    try:
        model_name = "bert-base-chinese"
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertModel.from_pretrained(model_name)
        app.state.bert_tokenizer = tokenizer
        app.state.bert_model = model
        print("BERT model loaded successfully.")
    except Exception as e:
        print(f"Error loading BERT model: {e}")
        app.state.bert_tokenizer = None
        app.state.bert_model = None

    yield

    # --- Shutdown ---
    print("Application shutdown.")
    # No explicit shutdown needed for firebase-admin or the BERT model


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
