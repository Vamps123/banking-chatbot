from pathlib import Path
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings

class VectorStore:
    def __init__(self):
        persistence_path = Path(settings.vector_store_dir)
        persistence_path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.Client(ChromaSettings(chroma_db_impl="duckdb+parquet", persist_directory=str(persistence_path)))
        self.collection = self.client.get_or_create_collection("banking_support")
        if not self.collection:
            self.collection = self.client.create_collection("banking_support")

    def add_documents(self, ids: list[str], documents: list[str], embeddings: list[list[float]], metadata: list[dict] | None = None) -> None:
        self.collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadata or [])
        self.client.persist()

    def query(self, query_embedding: list[float], top_k: int = 4) -> list[dict]:
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        ids = results.get("ids", [[]])[0] if results else []
        texts = results.get("documents", [[]])[0] if results else []
        distances = results.get("distances", [[]])[0] if results else []
        metadatas = results.get("metadatas", [[]])[0] if results else []

        raw = []
        for idx, score, text, metadata in zip(ids, distances, texts, metadatas):
            if idx is None or text is None:
                continue
            raw.append({
                "id": idx,
                "score": score,
                "text": text,
                "metadata": metadata or {},
            })
        return raw
