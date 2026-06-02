from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    province_code: str = Field(..., description="省份编码，如 beijing")
    province_name: str = Field(..., description="省份名称")
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    suggestions: list[str] = Field(default_factory=list)
