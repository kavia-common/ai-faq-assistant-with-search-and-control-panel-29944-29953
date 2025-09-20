# AI FAQ Assistant with Search and Control Panel

This repository contains a Python-based mini project featuring an AI FAQ Bot integrated with Retrieval-Augmented Generation (RAG) and a Model Control Panel (MCP).

- Backend: FastAPI (this folder: `faq_bot_backend`)
- Theme: Ocean Professional (blue & amber accents)

## Quickstart

Requirements:
- Python 3.9+ (recommended 3.11)
- pip

Install dependencies:

```bash
cd faq_bot_backend
pip install -r requirements.txt
```

Run the backend:

```bash
python -m api.main
# Or:
# python src/run.py
# Or with uvicorn:
# uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Open API docs:
- Swagger UI: http://localhost:8000/docs
- Themed docs landing: http://localhost:8000/themed-docs
- OpenAPI JSON: http://localhost:8000/openapi.json

Health check:
- GET http://localhost:8000/

## API Overview

- /api/faq/answer [POST]:
  - Request: { "query": "How do I reset my password?", "top_k": 3 }
  - Response: { "answer": "...", "contexts": [...], "model": "gpt-mini", "meta": {...} }

- /api/mcp/models [GET]:
  - Lists available models and shows the active model.

- /api/mcp/models/set [POST]:
  - Request: { "model": "gpt-balanced" }
  - Sets the active model for generation.

- /api/docs/websocket-usage [GET]:
  - Returns notes about potential WebSocket usage in future versions.

## Project Structure

```
faq_bot_backend/
  ├─ requirements.txt
  └─ src/
     ├─ api/
     │  ├─ __init__.py
     │  ├─ main.py
     │  ├─ config/
     │  │  └─ settings.py
     │  ├─ routers/
     │  │  ├─ __init__.py
     │  │  ├─ faq.py
     │  │  ├─ mcp.py
     │  │  └─ docs.py
     │  └─ services/
     │     ├─ __init__.py
     │     ├─ ai_service.py
     │     ├─ rag.py
     │     └─ vector_store.py
     └─ run.py
```

## Configuration

Environment variables:
- ENVIRONMENT: default `development`
- CORS_ALLOW_ORIGINS: default `*` (comma-separated list)

Create a `.env` file if needed (do not commit secrets). Example:

```
ENVIRONMENT=development
CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Ocean Professional Theme

The API exposes an `x-theme` section in OpenAPI JSON and a themed docs landing at `/themed-docs` to reflect:
- Primary: #2563EB (blue)
- Secondary: #F59E0B (amber)
- Error: #EF4444
- Background: #f9fafb
- Surface: #ffffff
- Text: #111827

## Notes

- The AI service is a stub and does not call external providers. Integrate your preferred LLM by updating `api/services/ai_service.py`.
- The RAG pipeline uses an in-memory TF cosine similarity for demonstration.

MIT License