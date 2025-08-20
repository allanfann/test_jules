import re

import torch
from fastapi import APIRouter, Depends, HTTPException, Request

from app.models.api import ApiResponse
from app.models.processing import (
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
    summary="使用 BERT 處理原始文字",
    tags=["Processing"],
)
async def text_processing(
    payload: TextProcessingRequest,
    tokenizer=Depends(get_bert_tokenizer),
    model=Depends(get_bert_model),
):
    """
    提交原始文字，使用預先訓練的 BERT 模型進行斷詞和嵌入。
    """
    inputs = tokenizer(
        payload.text, return_tensors="pt", truncation=True, max_length=512
    )
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    with torch.no_grad():
        outputs = model(**inputs)

    sentence_embedding = outputs.pooler_output[0].tolist()

    processed_data = {
        "original_text": payload.text,
        "tokens": tokens,
        "embedding_vector": sentence_embedding,
    }
    return ApiResponse(
        status="success",
        data=processed_data,
        message="已成功使用 BERT 處理文字。",
    )


@router.post(
    "/information-extraction",
    response_model=ApiResponse,
    summary="資訊擷取 (基於 BERT)",
    tags=["Processing"],
)
async def information_extraction(
    payload: InformationExtractionRequest,
    tokenizer=Depends(get_bert_tokenizer),
):
    """
    使用 BERT tokenizer 將詞語作為實體進行擷取。
    """
    inputs = tokenizer(
        payload.text, return_tensors="pt", truncation=True, max_length=512
    )
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    extracted_data = {"entities": tokens, "events": []}
    return ApiResponse(
        status="success",
        data=extracted_data,
        message="已使用 BERT tokenizer 擷取資訊。",
    )


@router.post(
    "/intent-classification",
    response_model=ApiResponse,
    summary="意圖分類",
    tags=["Processing"],
)
async def intent_classification(request: IntentClassificationRequest):
    """根據關鍵字對話語片段進行意圖分類。"""
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
        message="意圖分類成功。",
    )


@router.post(
    "/structured-conversion",
    response_model=ApiResponse,
    summary="轉換為結構化資料",
    tags=["Processing"],
)
async def structured_conversion(request: StructuredConversionRequest):
    """根據 schema 將非結構化文字轉換為結構化格式。"""
    patterns = [r"([^:]+):\s*(.*)"]

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
        message="文字已成功轉換為結構化格式。",
    )
