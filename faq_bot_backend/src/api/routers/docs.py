from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class WebsocketUsage(BaseModel):
    # PUBLIC_INTERFACE
    note: str = Field(..., description="General note about real-time usage.")
    example: str = Field(..., description="Example WebSocket path if used in future.")


@router.get(
    "/websocket-usage",
    response_model=WebsocketUsage,
    summary="WebSocket usage note",
    description="Provides a general note about real-time connections for future expansion. No active WebSocket endpoints in this service.",
    operation_id="websocket_usage_note",
)
def websocket_usage_note():
    """
    PUBLIC_INTERFACE
    Returns general usage notes for WebSocket connections to be added in future.
    """
    return WebsocketUsage(
        note="This service currently does not expose WebSocket endpoints. Future versions may stream tokens.",
        example="wss://<host>/ws/stream"
    )
