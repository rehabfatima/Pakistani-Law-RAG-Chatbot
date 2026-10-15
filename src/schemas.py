from pydantic import BaseModel, Field
from typing import List


class RetrievedChunk(BaseModel):
    """Represents one chunk retrieved from the legal document."""

    text: str
    section: str
    chunk_id: str
    distance: float


class QueryRequest(BaseModel):
    """Represents a user's question sent to the chatbot."""

    question: str = Field(..., min_length=1)


class ChatbotResponse(BaseModel):
    """Represents the final response returned by the RAG chatbot."""

    answer: str
    sources: List[RetrievedChunk]
    is_in_scope: bool
    retrieval_time_ms: float
    generation_time_ms: float