# Backend Service

This backend hosts the RAG pipeline and exposes the API endpoints used by the frontend.

## Endpoints

- `POST /chat` — send a user message and receive a grounded answer.
- `POST /upload` — upload a PDF, TXT, or DOCX document and index its content.
- `GET /health` — check service status.

## Local Run

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Ingestion

To ingest the sample dataset:

```powershell
cd backend
python scripts\ingest.py
```

## Environment

Copy `.env.example` to `.env` and add an optional `OPENAI_API_KEY`.
