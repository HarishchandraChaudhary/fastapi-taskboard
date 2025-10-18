from repositories.task_repository import TaskRepository
from schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus, ListTasksResponse
from entities.task import Task
from schemas.category import CategoryResponse
from fastapi import HTTPException, status

class CreateTaskUseCase:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def execute(self, task_data: TaskCreate) -> TaskResponse:
        """Creates a new task and its relationships."""
        task_entity = Task(**task_data.model_dump(exclude={"category_ids", "tag_ids"}))
        
        created_task = await self.task_repo.create_task(
            task_entity,
            task_data.category_ids,
            task_data.tag_ids
        )
        
        categories = await self.task_repo.get_task_categories(created_task.id)
        tags = await self.task_repo.get_task_tags(created_task.id)

        response = TaskResponse.model_validate(created_task)
        response.categories = [CategoryResponse.model_validate(c) for c in categories]
        response.tags = [CategoryResponse.model_validate(t) for t in tags] 
        
        return response

class UpdateTaskStatusUseCase:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def execute(self, task_id: str, status_update: TaskUpdateStatus) -> bool:
        """Updates a task's status."""
        success = await self.task_repo.update_task_status(task_id, status_update.status)
        if not success:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or already deleted")
        return True

class DeleteTaskUseCase:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def execute(self, task_id: str) -> bool:
        """Soft deletes a task."""
        success = await self.task_repo.soft_delete_task(task_id)
        if not success:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or already deleted")
        return True

class ListTasksUseCase:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def execute(self, filter_type: str | None, filter_id: str | None, cursor: str | None, limit: int) -> ListTasksResponse:
        """Lists tasks with optional filtering and cursor pagination."""
        
        tasks_list, next_cursor = await self.task_repo.list_tasks(filter_id, filter_type, cursor, limit)

        response_items = []
        for task in tasks_list:
            categories = await self.task_repo.get_task_categories(task.id)
            tags = await self.task_repo.get_task_tags(task.id)

            task_response = TaskResponse.model_validate(task)
            task_response.categories = [CategoryResponse.model_validate(c) for c in categories]
            task_response.tags = [CategoryResponse.model_validate(t) for t in tags]
            response_items.append(task_response)

        return ListTasksResponse(
            items=response_items,
            next_cursor=next_cursor
        )