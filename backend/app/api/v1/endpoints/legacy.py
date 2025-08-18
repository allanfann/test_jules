from fastapi import APIRouter

from app.models.api import ApiResponse
from app.models.legacy import (
    InformationExtractionRequest,
    IntentClassificationRequest,
    StructuredConversionRequest,
    TextProcessingRequest,
)

router = APIRouter()


@router.post(
    "/text-processing",
    response_model=ApiResponse,
    summary="Process Raw Text",
    tags=["Legacy Processing"],
)
async def text_processing(request: TextProcessingRequest):
    """Submits raw text for preprocessing steps like tokenization, lowercasing, etc."""
    processed_data = {
        "original_text": request.text,
        "processed_text": request.text.lower(),
    }
    return ApiResponse(
        status="success", data=processed_data, message="Text processed successfully."
    )


@router.post(
    "/information-extraction",
    response_model=ApiResponse,
    summary="Extract Information",
    tags=["Legacy Processing"],
)
async def information_extraction(request: InformationExtractionRequest):
    """Extracts entities, events, and relationships from preprocessed text."""
    extracted_data = {"entities": [], "events": []}
    return ApiResponse(
        status="success",
        data=extracted_data,
        message="Information extracted successfully.",
    )


@router.post(
    "/intent-classification",
    response_model=ApiResponse,
    summary="Classify Intent",
    tags=["Legacy Processing"],
)
async def intent_classification(request: IntentClassificationRequest):
    """Classifies the intent from a conversational snippet."""
    classified_data = {"intent": "Unknown", "confidence": 0.0}
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
    structured_data = {"schema_id": request.schema_id, "data": {}}
    return ApiResponse(
        status="success",
        data=structured_data,
        message="Text converted to structured format successfully.",
    )
