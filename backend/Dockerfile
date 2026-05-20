FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
EXPOSE 8000
ENV CHROMA_DB_DIR=/app/chromadb

# Ingestion is memory-heavy (downloads embedding/LLM artifacts). Default: OFF.
# Enable explicitly via RUN_INGEST=1.
ENV RUN_INGEST=0

CMD ["sh", "-c", "if [ "$RUN_INGEST" = "1" ]; then python scripts/ingest.py; fi && uvicorn app.main:app --host 0.0.0.0 --port 8000"]


