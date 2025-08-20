import logging
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

# Configure logger
logger = logging.getLogger(__name__)

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
    遍歷決策樹。

    本 API 用於導覽和遍歷決策樹。使用者可以透過提供決策樹 ID 來開始，
    或透過提供當前節點 ID 和答案來繼續遍歷。

    - **若要開始一個新的決策樹遍歷**：
      - 只需在請求中提供 `tree_id`。
      - API 將會回傳決策樹的根節點。

    - **若要繼續遍歷**：
      - 在請求中提供 `tree_id`、`current_node_id` 和 `answer`。
      - `answer` 必須是 `possible_answers` 列表中的一個有效選項。
      - API 將根據您的答案回傳下一個節點。

    - **節點類型**：
      - **DECISION**：表示這是一個決策節點，您需要從 `possible_answers` 中選擇一個答案。
      - **OUTCOME**：表示這是一個結果節點，遍歷在此結束。

    **參數說明**:
    - `request`: 一個包含以下欄位的 JSON 物件：
      - `tree_id` (str): 必要欄位，指定要遍歷的決策樹 ID。
      - `current_node_id` (str, 可選): 當前節點的 ID。若為空，則從根節點開始。
      - `answer` (str, 可選): 使用者對當前節點問題的回答。

    **回傳值**:
    - 一個 `ApiResponse` 物件，其中 `data` 欄位包含一個 `DecisionResponseData` 物件，
      描述了當前或下一個節點的詳細資訊。

    **可能的錯誤**:
    - `400 Bad Request`:
      - 當提供了 `current_node_id` 卻未提供 `answer` 時。
      - 當 `answer` 不是目前節點的有效選項時。
      - 當前節點不是一個決策節點時。
    - `404 Not Found`:
      - 當 `tree_id` 或 `current_node_id` 不存在時。
    - `503 Service Unavailable`:
      - 當無法連接到後端服務 (例如 Firestore) 時。
    - `500 Internal Server Error`:
      - 發生其他非預期的伺服器錯誤時。
    """
    logger.info(f"收到 /decide 的請求: {request.dict()}")
    try:
        engine = DecisionTreeEngine(db)
        logger.debug("DecisionTreeEngine 已初始化。")

        if not request.current_node_id:
            logger.info(f"開始新的遍歷，決策樹 ID: {request.tree_id}")
            node_data = engine.get_start_node(request.tree_id)
            logger.info(f"成功取得起始節點: {node_data.get('id')}")
        else:
            logger.info(
                f"繼續遍歷，決策樹 ID: {request.tree_id}, "
                f"節點 ID: {request.current_node_id}, 答案: {request.answer}"
            )
            if not request.answer:
                logger.warning(
                    "當提供了 'current_node_id' 時，'answer' 是必要欄位。"
                )
                raise HTTPException(
                    status_code=400,
                    detail="'answer' is required when 'current_node_id' is provided.",
                )
            node_data = engine.get_next_node(
                request.tree_id, request.current_node_id, request.answer
            )
            logger.info(f"成功取得下一個節點: {node_data.get('id')}")

        logger.debug(f"取得的節點資料: {node_data}")

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
        logger.info(f"成功格式化回應資料: {response_data.dict()}")

        return ApiResponse(status="success", data=response_data.dict())

    except (TreeNotFound, NodeNotFound) as e:
        logger.error(f"找不到錯誤: {e}", exc_info=True)
        raise HTTPException(status_code=404, detail=str(e))
    except (InvalidAnswer, NotDecisionNode) as e:
        logger.error(f"請求無效錯誤: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        logger.critical(f"連線錯誤: {e}", exc_info=True)
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.critical(f"發生未預期的錯誤: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"發生未預期的錯誤: {e}"
        )
