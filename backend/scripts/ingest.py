from pathlib import Path
from app.services.rag_service import RagService
from app.services.document_service import DocumentService
from app.core.config import settings

if __name__ == "__main__":
    print("Starting sample ingestion...")
    source_path = Path(__file__).resolve().parents[1] / "data" / "banking_faqs.txt"
    with open(source_path, "r", encoding="utf-8") as f:
        text = f.read()

    service = RagService()
    chunks = DocumentService.chunk_text(text, settings.max_chunk_size, settings.chunk_overlap)
    print(f"Ingesting {len(chunks)} document chunks from {source_path.name}...")
    service.ingest_chunks(chunks, source_path.name)
    print("Ingestion complete. Vector store persisted at:", settings.vector_store_dir)
