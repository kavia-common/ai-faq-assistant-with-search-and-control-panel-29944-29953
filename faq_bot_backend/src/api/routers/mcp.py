from typing import List, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.ai_service import AIService

router = APIRouter()

_ai_service = AIService()


class ModelInfo(BaseModel):
    # PUBLIC_INTERFACE
    name: str = Field(..., description="Model identifier.")
    description: str = Field(..., description="Human-friendly description.")


class ListModelsResponse(BaseModel):
    # PUBLIC_INTERFACE
    models: List[ModelInfo] = Field(..., description="Available models.")
    active_model: str = Field(..., description="Currently active model.")


class SetModelRequest(BaseModel):
    # PUBLIC_INTERFACE
    model: str = Field(..., description="Model name to set as active.")


@router.get(
    "/models",
    response_model=ListModelsResponse,
    summary="List available models",
    description="Returns available model choices and indicates the active model.",
)
def list_models() -> ListModelsResponse:
    """
    PUBLIC_INTERFACE
    List models endpoint for the Model Control Panel (MCP).
    """
    models = [
        ModelInfo(name=m["name"], description=m["description"])
        for m in _ai_service.get_available_models()
    ]
    return ListModelsResponse(models=models, active_model=_ai_service.get_active_model())


@router.post(
    "/models/set",
    response_model=Dict[str, str],
    summary="Set active model",
    description="Sets the active model to be used for generation.",
)
def set_model(payload: SetModelRequest):
    """
    PUBLIC_INTERFACE
    Sets the active model for generation.

    Raises HTTP 400 if the model does not exist.
    """
    ok = _ai_service.set_active_model(payload.model)
    if not ok:
        raise HTTPException(status_code=400, detail="Requested model is not available")
    return {"status": "ok", "active_model": _ai_service.get_active_model()}
