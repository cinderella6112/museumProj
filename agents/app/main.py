from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import ChatRequest, ChatResponse
from app.province_agent import generate_reply

app = FastAPI(
    title="Museum Province Agent",
    description="博物馆推荐省级智能体服务",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    reply, suggestions = generate_reply(
        request.province_code,
        request.province_name,
        request.message,
    )
    return ChatResponse(reply=reply, suggestions=suggestions)
