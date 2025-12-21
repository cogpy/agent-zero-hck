"""
Transform Quirk Endpoints

Endpoints for Toga's transform quirk functionality.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ..services.session_manager import SessionManager
from ..dependencies import (
    get_api_key,
    get_session_manager,
    rate_limit_default,
)


router = APIRouter()


class AbsorbedItem(BaseModel):
    """An item absorbed by the transform quirk."""

    id: str
    name: str
    type: str = Field(description="Type: code, pattern, style, etc.")
    source: Optional[str] = None
    absorbed_at: str
    usage_count: int = 0
    metadata: dict = Field(default_factory=dict)


class AbsorbRequest(BaseModel):
    """Request to absorb new content."""

    session_id: str
    content: str = Field(description="Content to absorb")
    content_type: str = Field(
        default="code", description="Type of content: code, pattern, style, persona"
    )
    name: Optional[str] = Field(default=None, description="Name for the absorbed item")
    source: Optional[str] = Field(default=None, description="Source of the content")


class TransformRequest(BaseModel):
    """Request to transform using absorbed content."""

    session_id: str
    item_id: str = Field(description="ID of absorbed item to use")
    target: str = Field(description="What to transform/apply to")
    intensity: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Transformation intensity"
    )


class TransformResult(BaseModel):
    """Result of a transformation."""

    success: bool
    transformed_content: str
    item_used: str
    intensity: float
    notes: Optional[str] = None


# Mock storage for absorbed items (in production, use database)
_absorbed_items: dict = {}


@router.get(
    "/{session_id}/absorbed",
    response_model=List[AbsorbedItem],
    summary="List absorbed items",
    description="Get all items absorbed by the transform quirk.",
)
async def list_absorbed(
    session_id: str,
    content_type: Optional[str] = None,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    List all absorbed items.

    Optionally filter by content type.
    """
    session = await session_manager.get_session_internal(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    items = _absorbed_items.get(session_id, [])

    if content_type:
        items = [i for i in items if i.get("type") == content_type]

    return items


@router.post(
    "/absorb",
    response_model=AbsorbedItem,
    summary="Absorb content",
    description="Absorb new content into the transform quirk.",
)
async def absorb_content(
    request: AbsorbRequest,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Absorb new content.

    This allows Toga to learn and later transform using
    the absorbed patterns, code, or styles.
    """
    session = await session_manager.get_session_internal(request.session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {request.session_id}",
        )

    import uuid
    from datetime import datetime

    item_id = f"abs-{uuid.uuid4().hex[:8]}"
    item_name = request.name or f"Absorbed {request.content_type}"

    item = AbsorbedItem(
        id=item_id,
        name=item_name,
        type=request.content_type,
        source=request.source,
        absorbed_at=datetime.utcnow().isoformat(),
        usage_count=0,
        metadata={
            "content_preview": (
                request.content[:100] + "..."
                if len(request.content) > 100
                else request.content
            ),
            "content_length": len(request.content),
        },
    )

    if request.session_id not in _absorbed_items:
        _absorbed_items[request.session_id] = []

    _absorbed_items[request.session_id].append(item.model_dump())

    return item


@router.post(
    "/transform",
    response_model=TransformResult,
    summary="Transform content",
    description="Transform content using an absorbed item.",
)
async def transform_content(
    request: TransformRequest,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Transform content using absorbed patterns.

    This applies the learned patterns/styles from an
    absorbed item to new content.
    """
    session = await session_manager.get_session_internal(request.session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {request.session_id}",
        )

    # Find the absorbed item
    items = _absorbed_items.get(request.session_id, [])
    item = next((i for i in items if i["id"] == request.item_id), None)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Absorbed item not found: {request.item_id}",
        )

    # Mock transformation (in production, use actual transformation logic)
    transformed = f"[Transformed with {item['name']} at {request.intensity*100:.0f}% intensity]\n{request.target}"

    # Update usage count
    item["usage_count"] += 1

    return TransformResult(
        success=True,
        transformed_content=transformed,
        item_used=item["name"],
        intensity=request.intensity,
        notes=f"Applied {item['type']} transformation",
    )


@router.delete(
    "/{session_id}/absorbed/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete absorbed item",
    description="Remove an absorbed item from the quirk.",
)
async def delete_absorbed(
    session_id: str,
    item_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Delete an absorbed item.
    """
    session = await session_manager.get_session_internal(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    items = _absorbed_items.get(session_id, [])
    original_len = len(items)
    _absorbed_items[session_id] = [i for i in items if i["id"] != item_id]

    if len(_absorbed_items[session_id]) == original_len:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Absorbed item not found: {item_id}",
        )


@router.get(
    "/{session_id}/stats",
    summary="Get quirk stats",
    description="Get statistics about the transform quirk usage.",
)
async def get_quirk_stats(
    session_id: str,
    api_key: str = Depends(get_api_key),
    session_manager: SessionManager = Depends(get_session_manager),
    _: None = Depends(rate_limit_default),
):
    """
    Get transform quirk statistics.
    """
    session = await session_manager.get_session_internal(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}",
        )

    items = _absorbed_items.get(session_id, [])

    type_counts = {}
    total_uses = 0
    for item in items:
        t = item.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
        total_uses += item.get("usage_count", 0)

    return {
        "total_absorbed": len(items),
        "by_type": type_counts,
        "total_transformations": total_uses,
        "capacity": {
            "current": len(items),
            "max": 100,  # Arbitrary limit
            "percentage": len(items) / 100 * 100,
        },
    }
