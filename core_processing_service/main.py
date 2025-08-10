from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# --- Pydantic Models for API Requests and Responses ---

class TextProcessingRequest(BaseModel):
    text: str = Field(..., description="待處理的原始文字內容。")
    tenant_id: str = Field(..., description="識別發出請求的租戶。")
    parameters: Optional[Dict[str, Any]] = Field(None, description="處理配置。")

class InformationExtractionRequest(BaseModel):
    text: str = Field(..., description="待處理的原始文字內容。")
    tenant_id: str = Field(..., description="識別發出請求的租戶。")

class IntentClassificationRequest(BaseModel):
    text: str = Field(..., description="待處理的原始文字內容。")
    tenant_id: str = Field(..., description="識別發出請求的租戶。")
    correlation_id: Optional[str] = Field(None, description="用於追蹤請求的唯一識別碼。")

class StructuredConversionRequest(BaseModel):
    text: str = Field(..., description="待處理的原始文字內容。")
    tenant_id: str = Field(..., description="識別發出請求的租戶。")
    schema_id: str = Field(..., description="指定的結構化格式 ID。")

class ApiResponse(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    errors: Optional[List[Dict[str, Any]]] = None


# --- FastAPI Application ---

app = FastAPI(
    title="Core Processing Service",
    description="A service for processing unstructured text data as per the system specification.",
    version="0.1.0",
)

@app.get("/health", summary="Health Check", tags=["Monitoring"])
def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    return {"status": "ok"}

@app.post("/api/v1/text-processing", response_model=ApiResponse, summary="Process Raw Text", tags=["Processing"])
async def text_processing(request: TextProcessingRequest):
    """
    Submits raw text for preprocessing steps like tokenization, lowercasing, etc.
    """
    # Placeholder for business logic
    processed_data = {
        "original_text": request.text,
        "processed_text": request.text.lower(), # Example processing
        "tokens": request.text.lower().split() # Example tokenization
    }
    return ApiResponse(status="success", data=processed_data, message="Text processed successfully.")

@app.post("/api/v1/information-extraction", response_model=ApiResponse, summary="Extract Information", tags=["Processing"])
async def information_extraction(request: InformationExtractionRequest):
    """
    Extracts entities, events, and relationships from preprocessed text.
    """
    # Placeholder for business logic
    extracted_data = {
        "entities": [{"type": "PERSON", "text": "Tim Cook"}], # Example
        "events": [{"type": "Launch", "product": "iPhone 15"}] # Example
    }
    return ApiResponse(status="success", data=extracted_data, message="Information extracted successfully.")

@app.post("/api/v1/intent-classification", response_model=ApiResponse, summary="Classify Intent", tags=["Processing"])
async def intent_classification(request: IntentClassificationRequest):
    """
    Classifies the intent from a conversational snippet.
    """
    # Placeholder for business logic from spec example
    classified_data = {
      "intent": "Order_Status_Inquiry",
      "entities": {
        "order_id": "12345" # Example entity extraction
      },
      "confidence": 0.95
    }
    return ApiResponse(status="success", data=classified_data, message="Intent classified successfully.")

@app.post("/api/v1/structured-conversion", response_model=ApiResponse, summary="Convert to Structured Data", tags=["Processing"])
async def structured_conversion(request: StructuredConversionRequest):
    """
    Converts unstructured text into a structured format based on a schema.
    """
    # Placeholder for business logic
    structured_data = {
        "schema_id": request.schema_id,
        "data": {"product_name": "Example Product", "review": request.text} # Example
    }
    return ApiResponse(status="success", data=structured_data, message="Text converted to structured format successfully.")
