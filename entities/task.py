from datetime import datetime
from typing import Literal

TaskStatus = Literal["pending", "in_progress", "completed"]

class Task:
    def __init__(
        self,
        title: str,
        description: str,
        due_date: datetime,
        status: TaskStatus = "pending",
        deleted: bool = False,
        id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
        self.deleted = deleted
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

class Category:
    def __init__(
        self,
        name: str,
        description: str,
        id: str | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description

class Tag:
    def __init__(
        self,
        name: str,
        description: str,
        id: str | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description