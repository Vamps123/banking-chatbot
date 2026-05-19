from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=4)
    message: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    response: str
    source_chunks: list[str]
    session_id: str

class UploadResponse(BaseModel):
    filename: str
    status: str
    chunks_added: int

class UploadRequest(BaseModel):
    filename: str
    content: str
