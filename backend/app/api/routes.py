import logging
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.api.schemas import ChatRequest, ChatResponse, UploadResponse
from app.services.rag_service import RagService
from app.services.document_service import DocumentService
from app.core.config import settings

try:
    # Prefer relative import (works when backend is treated as a package)
    from .streaming_routes import router as streaming_router
except ModuleNotFoundError:
    # Fallback to absolute import (some deployment build contexts)
    from app.api.streaming_routes import router as streaming_router


router = APIRouter()

logger = logging.getLogger(__name__)

rag_service = RagService()

router.include_router(streaming_router)


def validate_upload_file(file: UploadFile) -> None:
    if file.content_type not in {"text/plain", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}:
        raise HTTPException(status_code=400, detail="Unsupported document type. Use PDF, TXT, or DOCX.")

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    logger.info("Received chat request for session %s", request.session_id)
    response, source_chunks = rag_service.answer(request.session_id, request.message)
    return ChatResponse(response=response, source_chunks=source_chunks, session_id=request.session_id)

@router.post("/upload", response_model=UploadResponse)
async def upload_endpoint(file: UploadFile = File(...)):
    validate_upload_file(file)
    content_bytes = await file.read()
    content = content_bytes.decode("utf-8", errors="ignore")
    if file.content_type == "application/pdf":
        text = DocumentService.extract_text_from_pdf(content_bytes)
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = DocumentService.extract_text_from_docx(content_bytes)
    else:
        text = content

    chunks = DocumentService.chunk_text(text, settings.max_chunk_size, settings.chunk_overlap)
    embeddings = rag_service.ingest_chunks(chunks, file.filename)
    return UploadResponse(filename=file.filename, status="ingested", chunks_added=len(chunks))

@router.get("/status")
def status():
    return JSONResponse({"status": "ready", "vector_store": settings.vector_store_dir})
