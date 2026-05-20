import logging
from typing import List
from uuid import uuid4
from app.models.embeddings import EmbeddingService
from app.models.vector_store import VectorStore
from app.services.memory_service import memory_service
from app.services.llm_service import LlmService
from app.core.config import settings

logger = logging.getLogger(__name__)

class RagService:
    def __init__(self):
        self.embeddings = EmbeddingService()
        self.vector_store = VectorStore()
        # Defer LLM creation to first request to reduce startup memory usage on small Render instances.
        self.llm_service = None

    def _get_llm(self) -> LlmService:
        if self.llm_service is None:
            self.llm_service = LlmService()
        return self.llm_service


    def ingest_chunks(self, chunks: List[str], source: str) -> int:
        ids = [f"{source}-{i}-{uuid4()}" for i in range(len(chunks))]
        embeddings = self.embeddings.embed_documents(chunks)
        metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]
        self.vector_store.add_documents(ids=ids, documents=chunks, embeddings=embeddings, metadata=metadatas)
        return len(chunks)

    def answer(self, session_id: str, user_query: str) -> tuple[str, List[str]]:
        memory_service.add_message(session_id, "user", user_query)
        query_embedding = self.embeddings.embed_query(user_query)
        hits = self.vector_store.query(query_embedding, top_k=settings.top_k)
        contexts = [hit["text"] for hit in hits if hit["text"]]
        source_chunks = [hit["text"][:240] for hit in hits]

        if not contexts:
            answer = "I couldn't find relevant information in the current knowledge base. Please upload a related document or ask a different question."
            memory_service.add_message(session_id, "assistant", answer)
            return answer, []

        prompt = self._build_prompt(user_query, memory_service.get_context(session_id), contexts)
        llm = self._get_llm()
        answer = llm.generate(prompt)
        memory_service.add_message(session_id, "assistant", answer)
        return answer, source_chunks


    def _build_prompt(self, query: str, session_context: str, retrieved_chunks: List[str]) -> str:
        context_section = "\n\n".join(retrieved_chunks).strip()
        prompt = (
            "You are an AI banking support assistant. Answer clearly using only the information provided in the context. "
            "If the answer cannot be found in the retrieved content, say that you cannot answer precisely and offer to ask a support representative.\n\n"
            f"Conversation history:\n{session_context}\n\n"
            f"Retrieved context:\n{context_section}\n\n"
            f"Customer question:\n{query}\n\n"
            "Provide a concise, factual answer grounded in the context above."
        )
        return prompt
