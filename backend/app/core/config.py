from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str | None = None
    llm_model: str = "gpt2"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_store_dir: str = str(Path("./chromadb").resolve())
    max_chunk_size: int = 900
    chunk_overlap: int = 150
    top_k: int = 4

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        fields = {
            "vector_store_dir": {"env": "CHROMA_DB_DIR"},
        }

settings = Settings()
