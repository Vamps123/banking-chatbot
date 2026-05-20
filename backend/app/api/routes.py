import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, Body, Request, Query


from fastapi.responses import JSONResponse
from app.api.schemas import ChatRequest, ChatResponse, UploadResponse
from app.services.rag_service import RagService
from app.services.document_service import DocumentService
from app.core.config import settings

# Streaming router is optional in some build contexts.
# If it can't be imported, the server still starts and /chat continues to work.
streaming_router = None
try:
    from .streaming_routes import router as _streaming_router

    streaming_router = _streaming_router
except ModuleNotFoundError:
    pass
except Exception:
    pass

# Absolute import fallback intentionally removed to avoid breaking startup in
# containers where package discovery differs.



router = APIRouter()


logger = logging.getLogger(__name__)

rag_service = RagService()

# Instantiate a lightweight service at import time; heavy models are lazily loaded
# by RagService to keep Render boot memory usage low.


if streaming_router is not None:
    router.include_router(streaming_router)



def validate_upload_file(file: UploadFile) -> None:
    if file.content_type not in {"text/plain", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}:
        raise HTTPException(status_code=400, detail="Unsupported document type. Use PDF, TXT, or DOCX.")

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: Request,
    session_id: str | None = Query(default=None),
    message: str | None = Query(default=None),
):
    """Chat endpoint.

    This version primarily uses query params (session_id, message) to avoid JSON-body
    parsing issues on some proxies.
    """

    # If query params are missing, try (optionally) to read JSON body.
    if (session_id is None or message is None) and request.headers.get("content-type", "").startswith("application/json"):
        try:
            body = await request.json()
            if isinstance(body, dict):
                session_id = session_id or body.get("session_id")
                message = message or body.get("message")
        except Exception:
            pass

    if not session_id or not isinstance(session_id, str):
        raise HTTPException(status_code=422, detail="Missing/invalid session_id")
    if not message or not isinstance(message, str):
        raise HTTPException(status_code=422, detail="Missing/invalid message")

    logger.info("Received chat request for session %s", session_id)
    response, source_chunks = rag_service.answer(session_id, message)
    return ChatResponse(response=response, source_chunks=source_chunks, session_id=session_id)




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
