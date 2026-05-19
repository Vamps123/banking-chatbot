from io import BytesIO
from typing import List
from pypdf import PdfReader
import docx
import re

class DocumentService:
    @staticmethod
    def extract_text_from_pdf(pdf_bytes: bytes) -> str:
        reader = PdfReader(BytesIO(pdf_bytes))
        fragments = []
        for page in reader.pages:
            text = page.extract_text() or ""
            fragments.append(text.strip())
        return "\n\n".join(fragments)

    @staticmethod
    def extract_text_from_docx(docx_bytes: bytes) -> str:
        doc = docx.Document(BytesIO(docx_bytes))
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)

    @staticmethod
    def sanitize_text(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def chunk_text(text: str, max_size: int, overlap: int) -> List[str]:
        cleaned = DocumentService.sanitize_text(text)
        tokens = cleaned.split(" ")
        chunks = []
        start = 0
        while start < len(tokens):
            end = min(start + max_size, len(tokens))
            chunk = " ".join(tokens[start:end]).strip()
            chunks.append(chunk)
            start += max_size - overlap
        return chunks
