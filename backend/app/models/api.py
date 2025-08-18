from typing import Any, Dict, List

from pydantic import BaseModel


class ApiResponse(BaseModel):
    status: str
    data: Any | None = None
    message: str | None = None
    errors: List[Dict[str, Any]] | None = None
