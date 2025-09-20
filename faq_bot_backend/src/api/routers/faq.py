from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.rag import RagPipeline
from ..services.ai_service import AIService
from ..config.settings import get_settings

router = APIRouter()

# Instantiate services (simple module-level for this small project)
_settings = get_settings()
_ai_service = AIService()
_rag_pipeline = RagPipeline(settings=_settings, ai_service=_ai_service)


class FaqAnswerRequest(BaseModel):
    # PUBLIC_INTERFACE
    query: str = Field(..., description="User question to be answered.")
    top_k: int = Field(3, description="Number of relevant context chunks to retrieve.")


class ContextChunk(BaseModel):
    source: str = Field(..., description="Source identifier of the context (e.g., filename or doc id).")
    score: float = Field(..., description="Similarity score.")
    text: str = Field(..., description="Context text snippet.")


class FaqAnswerResponse(BaseModel):
    # PUBLIC_INTERFACE
    answer: str = Field(..., description="Generated answer from the AI model.")
    contexts: List[ContextChunk] = Field(default_factory=list, description="Retrieved supporting context chunks.")
    model: str = Field(..., description="Model used for generation.")
    meta: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the generation.")


@router.post(
    "/answer",
    response_model=FaqAnswerResponse,
    summary="Get an answer to an FAQ using RAG",
    description="Retrieves relevant context using RAG and generates an answer using the configured AI model.",
    responses={
        200: {"description": "Answer successfully generated."},
        400: {"description": "Invalid input."},
        500: {"description": "Generation failed."},
    },
)
def get_answer(payload: FaqAnswerRequest) -> FaqAnswerResponse:
    """
    PUBLIC_INTERFACE
    Generate an answer for the user query using RAG and the current model.

    Parameters:
    - payload: FaqAnswerRequest containing the query and optional top_k

    Returns:
    - FaqAnswerResponse including answer text, contexts used, model name, and metadata.

    Raises:
    - HTTPException(500) if generation fails.
    """
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")

    contexts = _rag_pipeline.retrieve(payload.query, top_k=payload.top_k)
    try:
        answer, meta = _rag_pipeline.generate_with_context(payload.query, contexts)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}") from exc

    return FaqAnswerResponse(
        answer=answer,
        contexts=[ContextChunk(**c) for c in contexts],
        model=_ai_service.get_active_model(),
        meta=meta,
    )
