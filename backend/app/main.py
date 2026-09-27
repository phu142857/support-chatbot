from fastapi import FastAPI

from app.api.chat import router as chat_router


app = FastAPI(
    title="Support Chatbot API",
    description="AI-powered support chatbot for screenshot-based issue resolution",
    version="1.0.0",
)

app.include_router(chat_router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "support-chatbot-api",
    }