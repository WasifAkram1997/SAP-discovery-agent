"""Pydantic models for FastAPI request/response."""

from pydantic import BaseModel, Field


# class ChatRequest(BaseModel):
#     """Request model for chat endpoint."""

#     message: str = Field(..., description="User's chat message")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str = Field(..., description="Agent's response message")
