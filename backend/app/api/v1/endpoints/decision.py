from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import firestore

from app.core.firebase_setup import get_firestore_db
from app.models.api import ApiResponse
from app.models.decision import DecisionRequest, DecisionResponseData
from app.services.tree_engine import (
    DecisionTreeEngine,
    InvalidAnswer,
    NodeNotFound,
    NotDecisionNode,
    TreeNotFound,
)

router = APIRouter()


@router.post(
    "/decide",
    response_model=ApiResponse,
    summary="Traverse a Decision Tree",
    tags=["Decision Trees"],
)
async def decide(
    request: DecisionRequest, db: firestore.Client = Depends(get_firestore_db)
):
    """
    Traverses a decision tree. Provide just the `tree_id` to start.
    Provide `tree_id`, `current_node_id`, and `answer` to proceed to the next step.
    """
    try:
        engine = DecisionTreeEngine(db)

        if not request.current_node_id:
            # Start a new tree traversal from the root
            node_data = engine.get_start_node(request.tree_id)
        else:
            # Continue traversal to the next node
            if not request.answer:
                raise HTTPException(
                    status_code=400,
                    detail="'answer' is required when 'current_node_id' is provided.",
                )
            node_data = engine.get_next_node(
                request.tree_id, request.current_node_id, request.answer
            )

        # Format the successful response
        response_data = DecisionResponseData(
            tree_id=request.tree_id,
            node_id=node_data.get("id"),
            node_type=node_data.get("type"),
            text=node_data.get("text"),
            possible_answers=[
                child["answer_text"] for child in node_data.get("children", [])
            ]
            if node_data.get("type") == "DECISION"
            else None,
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
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )
