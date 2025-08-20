from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


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
    correlation_id: Optional[str] = Field(
        None, description="用於追蹤請求的唯一識別碼。"
    )


class StructuredConversionRequest(BaseModel):
    text: str = Field(..., description="待處理的原始文字內容。")
    tenant_id: str = Field(..., description="識別發出請求的租戶。")
    schema_id: str = Field(..., description="指定的結構化格式 ID。")
