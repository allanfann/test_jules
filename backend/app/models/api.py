from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    status: str
    data: Any | None = None
    message: str | None = None
    errors: List[Dict[str, Any]] | None = None


class PersonalityAnalysisRequest(BaseModel):
    text: str


class PersonalityAnalysisResponse(BaseModel):
    personality: str
    scores: Dict[str, int]


class MbtiAnalysisRequest(BaseModel):
    answers: List[str] = Field(
        ...,
        description="A list of answers representing MBTI dimension choices.",
        example=["E", "S", "T", "J"],
    )


class MbtiAnalysisResponse(BaseModel):
    mbti_type: str = Field(..., description="The calculated MBTI type.")
    summary: str = Field(..., description="A brief summary of the MBTI type.")
    description: str = Field(..., description="A detailed description of the MBTI type.")
