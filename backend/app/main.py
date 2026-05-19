from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.logger import configure_logger
from app.core.config import settings

configure_logger()
app = FastAPI(
    title="GenAI Banking Support Chatbot",
    description="RAG-powered banking assistant API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model": settings.llm_model,
        "vector_store": settings.vector_store_dir,
    }
