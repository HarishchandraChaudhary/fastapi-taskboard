from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Literal

from entities.task import TaskStatus
from schemas.category import CategoryResponse

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=120)
    description: str = Field(..., max_length=1000)
    due_date: datetime
    category_ids: list[str] = Field(default_factory=list)
    tag_ids: list[str] = Field(default_factory=list)

class TaskUpdateStatus(BaseModel):
    status: TaskStatus

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    due_date: datetime
    status: TaskStatus
    deleted: bool
    created_at: datetime
    updated_at: datetime
    categories: list[CategoryResponse] = Field(default_factory=list)
    tags: list[CategoryResponse] = Field(default_factory=list) 

    model_config = ConfigDict(from_attributes=True)
    
class ListTasksResponse(BaseModel):
    items: list[TaskResponse]
    next_cursor: str | None = None