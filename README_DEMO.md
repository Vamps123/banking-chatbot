# Demo Video Script

## 1. Introduction (30 seconds)
- "This is the GenAI Banking Support Chatbot, a retrieval-augmented system for customer banking queries."
- "It combines document ingestion, semantic embedding search, and generative AI to provide grounded answers."

## 2. Architecture Summary (1 minute)
- "The frontend is a React chat interface served by Vite."
- "The backend is built with FastAPI and exposes `/chat`, `/upload`, and `/health`."
- "We store vector embeddings in ChromaDB and use a session memory layer to preserve short-term conversational context."

## 3. Walkthrough the User Flow (2 minutes)
- "Start the app and show the chat UI."
- "Ask a question like 'What is a personal loan?' and note the assistant answer."
- "Then ask a follow-up, for example: 'What is its interest rate?' The system resolves pronoun references by using session memory."
- "Upload a banking document and show the assistant retrieving new context from the uploaded content."

## 4. RAG Pipeline Explanation (2 minutes)
- "Document ingestion extracts text from TXT, PDF, and DOCX sources."
- "Text is chunked and encoded using sentence-transformers."
- "Chunks are stored in ChromaDB for semantic retrieval."
- "On each chat request, the system retrieves top-k relevant chunks and builds a grounding prompt for the LLM."

## 5. Deployment & Environment (1.5 minutes)
- "The backend can run in a Docker container, and the frontend builds into a static site."
- "We include `render.yaml` for Render deployment and `.env.example` templates for environment setup."
- "No secrets are hardcoded. The OpenAI key is optional and can be provided via environment variables."

## 6. Challenges and Future Improvements (1 minute)
- "A key challenge was keeping the response grounded in retrieved documents even when conversation history refers back to prior questions."
- "Future improvements include streaming responses, rating retrieval relevance, Redis caching, and role-based authentication."
