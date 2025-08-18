import re

import torch
from fastapi import APIRouter, Depends, HTTPException, Request

from app.models.api import ApiResponse
from app.models.legacy import (
    InformationExtractionRequest,
    IntentClassificationRequest,
    StructuredConversionRequest,
    TextProcessingRequest,
)

router = APIRouter()


def get_bert_model(request: Request):
    if (
        not hasattr(request.app.state, "bert_model")
        or request.app.state.bert_model is None
    ):
        raise HTTPException(status_code=503, detail="BERT model not loaded.")
    return request.app.state.bert_model


def get_bert_tokenizer(request: Request):
    if (
        not hasattr(request.app.state, "bert_tokenizer")
        or request.app.state.bert_tokenizer is None
    ):
        raise HTTPException(status_code=503, detail="BERT tokenizer not loaded.")
    return request.app.state.bert_tokenizer


@router.post(
    "/text-processing",
    response_model=ApiResponse,
    summary="Process Raw Text using BERT",
    tags=["Legacy Processing"],
)
async def text_processing(
    payload: TextProcessingRequest,
    tokenizer=Depends(get_bert_tokenizer),
    model=Depends(get_bert_model),
):
    """
    Submits raw text for tokenization and embedding using a pre-trained BERT model.
    """
    # Tokenize the text
    inputs = tokenizer(
        payload.text, return_tensors="pt", truncation=True, max_length=512
    )
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    # Get embeddings
    with torch.no_grad():
        outputs = model(**inputs)

    # Use the embedding of the [CLS] token as the sentence representation
    sentence_embedding = outputs.pooler_output[0].tolist()

    processed_data = {
        "original_text": payload.text,
        "tokens": tokens,
        "embedding_vector": sentence_embedding,  # Renamed from tfidf_vector
    }
    return ApiResponse(
        status="success",
        data=processed_data,
        message="Text processed successfully with BERT.",
    )


@router.post(
    "/information-extraction",
    response_model=ApiResponse,
    summary="Extract Information (BERT based)",
    tags=["Legacy Processing"],
)
async def information_extraction(
    payload: InformationExtractionRequest,
    tokenizer=Depends(get_bert_tokenizer),
):
    """
    Extracts tokens as entities using the BERT tokenizer.
    Note: This is a basic implementation. For true NER, a fine-tuned model is needed.
    """
    inputs = tokenizer(
        payload.text, return_tensors="pt", truncation=True, max_length=512
    )
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    # For now, we'll consider all tokens as "entities" and have no "events"
    # This is a placeholder until a proper NER model is integrated.
    extracted_data = {"entities": tokens, "events": []}
    return ApiResponse(
        status="success",
        data=extracted_data,
        message="Information extracted using BERT tokenizer.",
    )


@router.post(
    "/intent-classification",
    response_model=ApiResponse,
    summary="Classify Intent",
    tags=["Legacy Processing"],
)
async def intent_classification(request: IntentClassificationRequest):
    """Classifies the intent from a conversational snippet based on keywords."""
    intents = {
        "greeting": ["你好", "您好", "嗨", "哈囉"],
        "goodbye": ["再見", "掰掰"],
        "weather_inquiry": ["天氣", "氣溫", "下雨", "晴天"],
    }

    classified_intent = "Unknown"
    confidence = 0.0

    for intent, keywords in intents.items():
        if any(keyword in request.text for keyword in keywords):
            classified_intent = intent
            confidence = 1.0
            break

    classified_data = {"intent": classified_intent, "confidence": confidence}
    return ApiResponse(
        status="success",
        data=classified_data,
        message="Intent classified successfully.",
    )


@router.post(
    "/structured-conversion",
    response_model=ApiResponse,
    summary="Convert to Structured Data",
    tags=["Legacy Processing"],
)
async def structured_conversion(request: StructuredConversionRequest):
    """Converts unstructured text into a structured format based on a schema."""
    # Simple key-value extraction using regex
    # Looks for patterns like "key: value" or "key is value"
    patterns = [r"(.*?):\s*(.*)", r"(.*?)\s+是\s+(.*)"]

    data = {}
    for line in request.text.split("\n"):
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                data[key] = value
                break

    structured_data = {"schema_id": request.schema_id, "data": data}
    return ApiResponse(
        status="success",
        data=structured_data,
        message="Text converted to structured format successfully.",
    )
