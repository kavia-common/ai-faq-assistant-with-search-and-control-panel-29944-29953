from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.responses import HTMLResponse

from .routers.faq import router as faq_router
from .routers.mcp import router as mcp_router
from .routers.docs import router as docs_router
from .config.settings import get_settings

# Initialize settings
settings = get_settings()

app = FastAPI(
    title="AI FAQ Bot Backend",
    description=(
        "Backend service for the AI FAQ Bot with Retrieval-Augmented Generation (RAG) and a Model Control Panel (MCP). "
        "Use the /api endpoints to retrieve answers and manage the model configuration."
    ),
    version="1.0.0",
    contact={
        "name": "AI FAQ Bot Team",
        "url": "https://example.com",
    },
    license_info={"name": "MIT"},
    openapi_tags=[
        {
            "name": "Health",
            "description": "Service health and basic information.",
        },
        {
            "name": "FAQ",
            "description": "Endpoints for FAQ answering using RAG + AI generation.",
        },
        {
            "name": "MCP",
            "description": "Model Control Panel endpoints for configuration and management.",
        },
        {
            "name": "Docs",
            "description": "Documentation helpers and themed Swagger UI notes.",
        },
    ],
)

# CORS for local dev and broad compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"], summary="Health Check", operation_id="health_check")
def health_check():
    """
    PUBLIC_INTERFACE
    Health check endpoint.
    Returns a simple payload indicating the service is healthy.
    """
    return {"message": "Healthy", "service": "AI FAQ Bot Backend", "version": "1.0.0"}


# Mount routers with prefixes
api_router = APIRouter(prefix="/api")
api_router.include_router(faq_router, prefix="/faq", tags=["FAQ"])
api_router.include_router(mcp_router, prefix="/mcp", tags=["MCP"])
api_router.include_router(docs_router, prefix="/docs", tags=["Docs"])
app.include_router(api_router)


# Custom OpenAPI generator to inject theme metadata (Ocean Professional style hints)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Inject simple theme metadata for clients/swagger customization
    openapi_schema["x-theme"] = {
        "name": "Ocean Professional",
        "colors": {
            "primary": "#2563EB",   # blue-600
            "secondary": "#F59E0B", # amber-500
            "error": "#EF4444",
            "background": "#f9fafb",
            "surface": "#ffffff",
            "text": "#111827",
        },
        "notes": "Apply blue accents for primary actions and amber for emphasis within API docs UI."
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore


@app.get("/themed-docs", include_in_schema=False)
async def themed_docs():
    """
    A simple themed container page that links to Swagger UI, hinting the Ocean Professional theme.
    """
    # This does not replace Swagger UI but gives a minimal themed landing to the docs.
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI FAQ Bot API Docs</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <style>
                :root {
                  --primary: #2563EB;
                  --secondary: #F59E0B;
                  --bg: #f9fafb;
                  --surface: #ffffff;
                  --text: #111827;
                }
                body {
                  margin: 0;
                  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
                  background: var(--bg);
                  color: var(--text);
                }
                .container {
                  max-width: 880px;
                  margin: 40px auto;
                  padding: 24px;
                  background: linear-gradient(180deg, rgba(37,99,235,0.05), rgba(249,250,251,1));
                  border-radius: 14px;
                  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
                  border: 1px solid rgba(37,99,235,0.15);
                }
                h1 {
                  color: var(--primary);
                  margin-top: 0;
                }
                p em {
                  color: var(--secondary);
                  font-style: normal;
                  font-weight: 600;
                }
                a.button {
                  display: inline-block;
                  padding: 12px 18px;
                  background: var(--primary);
                  color: white;
                  border-radius: 10px;
                  text-decoration: none;
                  transition: transform 0.06s ease, box-shadow 0.2s ease, background 0.2s ease;
                  box-shadow: 0 8px 20px rgba(37,99,235,0.35);
                }
                a.button:hover {
                  transform: translateY(-1px);
                  background: #1d4ed8;
                  box-shadow: 0 12px 28px rgba(37,99,235,0.45);
                }
                .note {
                  margin-top: 14px;
                  color: #374151;
                }
            </style>
        </head>
        <body>
            <div class="container">
              <h1>AI FAQ Bot API Documentation</h1>
              <p>This backend uses the <em>Ocean Professional</em> theme with blue and amber accents.</p>
              <a class="button" href="/docs">Open Swagger UI</a>
              <div class="note">
                Tip: Look for blue primary highlights and amber emphasis for key interactive elements.
              </div>
            </div>
        </body>
        </html>
        """
    )
