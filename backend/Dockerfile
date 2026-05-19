FROM python:3.12-slim
WORKDIR /app/backend
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./
EXPOSE 8000
ENV CHROMA_DB_DIR=/app/backend/chromadb
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
