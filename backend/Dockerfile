FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
EXPOSE 8000
ENV CHROMA_DB_DIR=/app/chromadb

# Ingest sample dataset (safe to run repeatedly).
# Do this at container start so Render always has vectors even if build cache or runtime filesystem differs.
CMD ["sh", "-c", "python scripts/ingest.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

