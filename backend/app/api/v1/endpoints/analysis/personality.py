from collections import Counter
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import firestore

from app.core.firebase_setup import get_firestore_db
from app.models.api import (
    ApiResponse,  # Import ApiResponse
    MbtiAnalysisRequest,
    MbtiAnalysisResponse,
    PersonalityAnalysisRequest,
    PersonalityAnalysisResponse,
)

router = APIRouter()

# --- MBTI Descriptions (can be moved to Firestore later) ---
MBTI_DESCRIPTIONS = {
    "INTJ": {
        "summary": "建築師 (The Architect)",
        "description": "富有想像力和策略性的思想家，凡事都有計畫。",
    },
    "INTP": {
        "summary": "邏輯學家 (The Logician)",
        "description": "具有創造力的發明家，對知識有著無法抑制的渴望。",
    },
    "ENTJ": {
        "summary": "指揮官 (The Commander)",
        "description": "大膽、富有想像力且意志堅強的領導者，總能找到或創造解決方法。",
    },
    "ENTP": {
        "summary": "辯論家 (The Debater)",
        "description": "聰明好奇的思想者，無法抗拒智力上的挑戰。",
    },
    "INFJ": {
        "summary": "提倡者 (The Advocate)",
        "description": "安靜而神秘，同時又鼓舞人心且不知疲倦的理想主義者。",
    },
    "INFP": {
        "summary": "調停者 (The Mediator)",
        "description": "詩意、善良和利他主義的人，總是願意幫助一個好的事業。",
    },
    "ENFJ": {
        "summary": "主人公 (The Protagonist)",
        "description": "富有魅力且鼓舞人心的領導者，有能力讓聽眾著迷。",
    },
    "ENFP": {
        "summary": "競選者 (The Campaigner)",
        "description": "熱情、有創造力且善於交際的自由精神，總能找到微笑的理由。",
    },
    "ISTJ": {
        "summary": "物流師 (The Logistician)",
        "description": "務實且注重事實的人，其可靠性無可懷疑。",
    },
    "ISFJ": {
        "summary": "守衛者 (The Defender)",
        "description": "非常敬業和熱情的保護者，隨時準備保衛他們所愛的人。",
    },
    "ESTJ": {
        "summary": "總經理 (The Executive)",
        "description": "出色的管理者，在管理事物或人員方面無與倫比。",
    },
    "ESFJ": {
        "summary": "執政官 (The Consul)",
        "description": "極其關心、善於交際且受歡迎的人，總是熱心幫助他人。",
    },
    "ISTP": {
        "summary": "鑒賞家 (The Virtuoso)",
        "description": "大膽而務實的實驗家，擅長使用各種工具。",
    },
    "ISFP": {
        "summary": "探險家 (The Adventurer)",
        "description": "靈活而迷人的藝術家，總是準備好探索和體驗新事物。",
    },
    "ESTP": {
        "summary": "企業家 (The Entrepreneur)",
        "description": "聰明、精力充沛且非常有感知力的人，真正享受生活在邊緣。",
    },
    "ESFP": {
        "summary": "表演者 (The Entertainer)",
        "description": "自發、精力充沛且熱情的表演者——在他們身邊，生活永遠不會無聊。",
    },
    "DEFAULT": {
        "summary": "無法確定的類型",
        "description": "您的答案無法對應到一個明確的 MBTI 類型。",
    },
}


def analyze_personality(text: str, personalities: Dict) -> Dict:
    """
    透過關鍵字匹配分析文本，以確定人格類型。
    這是一個簡化的原型實現。
    """
    scores = {p: 0 for p in personalities}

    lower_text = text.lower()

    for personality, data in personalities.items():
        for keyword in data.get("keywords", []):
            scores[personality] += lower_text.count(keyword)

    if all(score == 0 for score in scores.values()):
        dominant_personality = "realist"
    else:
        dominant_personality = max(scores, key=scores.get)

    return {"personality": dominant_personality.capitalize(), "scores": scores}


@router.post(
    "/personality_analysis",
    response_model=ApiResponse,
    summary="Analyze user personality from text",
    tags=["Analysis"],
)
async def personality_analysis(
    payload: PersonalityAnalysisRequest, db: firestore.Client = Depends(get_firestore_db)
):
    """
    對使用者輸入的文字進行簡單的人格分析。
    """
    personalities_ref = db.collection("personalities").stream()
    personalities = {doc.id: doc.to_dict() for doc in personalities_ref}
    analysis_result = analyze_personality(payload.text, personalities)
    response_data = PersonalityAnalysisResponse(**analysis_result)
    return ApiResponse(status="success", data=response_data)


@router.post(
    "/mbti_analysis",
    response_model=ApiResponse,
    summary="從答案分析 MBTI 類型",
    tags=["Analysis"],
)
async def mbti_analysis(payload: MbtiAnalysisRequest):
    """
    根據一系列答案計算 MBTI 人格類型。
    """
    answers = payload.answers
    if not answers or len(answers) < 4:
        raise HTTPException(
            status_code=400, detail="至少需要 4 個答案才能確定類型。"
        )

    counts = Counter(answers)

    mbti_type = ""
    mbti_type += "E" if counts.get("E", 0) >= counts.get("I", 0) else "I"
    mbti_type += "S" if counts.get("S", 0) >= counts.get("N", 0) else "N"
    mbti_type += "T" if counts.get("T", 0) >= counts.get("F", 0) else "F"
    mbti_type += "J" if counts.get("J", 0) >= counts.get("P", 0) else "P"

    result = MBTI_DESCRIPTIONS.get(mbti_type, MBTI_DESCRIPTIONS["DEFAULT"])

    response_data = MbtiAnalysisResponse(
        mbti_type=mbti_type,
        summary=result["summary"],
        description=result["description"],
    )
    return ApiResponse(status="success", data=response_data)
