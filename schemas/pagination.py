from pydantic import BaseModel, Field
from typing import TypeVar, Generic

T = TypeVar("T")

class CursorPageResponse(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None = Field(default=None, description="Base64 encoded string representing the next page cursor.")

class PaginationParams(BaseModel):
    limit: int = Field(default=10, le=50)
    cursor: str | None = None