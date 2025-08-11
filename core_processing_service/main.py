from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from tree_engine import DecisionTreeEngine, TreeNotFound, NodeNotFound, InvalidAnswer, NotDecisionNode

# --- Pydantic Models for API Requests and Responses ---

# Models for original processing endpoints
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

# Models for Decision Tree Endpoint
class DecisionRequest(BaseModel):
    tree_id: str = Field(..., description="The ID of the decision tree to interact with.")
    current_node_id: Optional[str] = Field(None, description="The ID of the current node. Omit to start from the root.")
    answer: Optional[str] = Field(None, description="The user's answer to the question of the current node.")

class DecisionResponseData(BaseModel):
    tree_id: str
    node_id: str
    node_type: str = Field(..., description="Either 'DECISION' or 'OUTCOME'.")
    text: str = Field(..., description="The question or the final outcome.")
    possible_answers: Optional[List[str]] = Field(None, description="A list of possible answers if the node is a 'DECISION' node.")

# Generic API Response Wrapper
class ApiResponse(BaseModel):
    status: str
    data: Optional[Any] = None
    message: Optional[str] = None
    errors: Optional[List[Dict[str, Any]]] = None


# --- FastAPI Application ---

app = FastAPI(
    title="Core Processing Service",
    description="A service for processing unstructured text data and traversing decision trees.",
    version="0.2.0", # Bump version for new feature
)

@app.get("/health", summary="Health Check", tags=["Monitoring"])
def health_check():
    """Health check endpoint to verify that the service is running."""
    return {"status": "ok"}

# --- Decision Tree Endpoint ---

@app.post("/api/v1/decide", response_model=ApiResponse, summary="Traverse a Decision Tree", tags=["Decision Trees"])
async def decide(request: DecisionRequest):
    """
    Traverses a decision tree. Provide just the `tree_id` to start.
    Provide `tree_id`, `current_node_id`, and `answer` to proceed to the next step.
    """
    try:
        engine = DecisionTreeEngine()

        if not request.current_node_id:
            # Start a new tree traversal from the root
            node_data = engine.get_start_node(request.tree_id)
        else:
            # Continue traversal to the next node
            if not request.answer:
                raise HTTPException(status_code=400, detail="'answer' is required when 'current_node_id' is provided.")
            node_data = engine.get_next_node(request.tree_id, request.current_node_id, request.answer)

        # Format the successful response
        response_data = DecisionResponseData(
            tree_id=request.tree_id,
            node_id=node_data.get('id'),
            node_type=node_data.get('type'),
            text=node_data.get('text'),
            possible_answers=[child['answer_text'] for child in node_data.get('children', [])] if node_data.get('type') == 'DECISION' else None
        )

        return ApiResponse(status="success", data=response_data.dict())

    except (TreeNotFound, NodeNotFound) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (InvalidAnswer, NotDecisionNode) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        # Catch-all for other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# --- Original Processing Endpoints (Placeholder) ---

@app.post("/api/v1/text-processing", response_model=ApiResponse, summary="Process Raw Text", tags=["Legacy Processing"])
async def text_processing(request: TextProcessingRequest):
    """Submits raw text for preprocessing steps like tokenization, lowercasing, etc."""
    processed_data = {"original_text": request.text, "processed_text": request.text.lower()}
    return ApiResponse(status="success", data=processed_data, message="Text processed successfully.")

@app.post("/api/v1/information-extraction", response_model=ApiResponse, summary="Extract Information", tags=["Legacy Processing"])
async def information_extraction(request: InformationExtractionRequest):
    """Extracts entities, events, and relationships from preprocessed text."""
    extracted_data = {"entities": [], "events": []}
    return ApiResponse(status="success", data=extracted_data, message="Information extracted successfully.")

@app.post("/api/v1/intent-classification", response_model=ApiResponse, summary="Classify Intent", tags=["Legacy Processing"])
async def intent_classification(request: IntentClassificationRequest):
    """Classifies the intent from a conversational snippet."""
    classified_data = {"intent": "Unknown", "confidence": 0.0}
    return ApiResponse(status="success", data=classified_data, message="Intent classified successfully.")

@app.post("/api/v1/structured-conversion", response_model=ApiResponse, summary="Convert to Structured Data", tags=["Legacy Processing"])
async def structured_conversion(request: StructuredConversionRequest):
    """Converts unstructured text into a structured format based on a schema."""
    structured_data = {"schema_id": request.schema_id, "data": {}}
    return ApiResponse(status="success", data=structured_data, message="Text converted to structured format successfully.")
