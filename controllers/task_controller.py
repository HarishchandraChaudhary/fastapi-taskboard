from fastapi import APIRouter, status, Query, Depends
from schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus, ListTasksResponse
from use_cases.task import (
    CreateTaskUseCase,
    UpdateTaskStatusUseCase,
    DeleteTaskUseCase,
    ListTasksUseCase,
)
from .base import get_container

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Dependency resolvers for use cases
def get_create_task_use_case(container=Depends(get_container)) -> CreateTaskUseCase:
    return container.resolve(CreateTaskUseCase)

def get_list_tasks_use_case(container=Depends(get_container)) -> ListTasksUseCase:
    return container.resolve(ListTasksUseCase)

def get_update_status_use_case(container=Depends(get_container)) -> UpdateTaskStatusUseCase:
    return container.resolve(UpdateTaskStatusUseCase)

def get_delete_task_use_case(container=Depends(get_container)) -> DeleteTaskUseCase:
    return container.resolve(DeleteTaskUseCase)

# Create task endpoint
@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Task with initial Category/Tag relationships"
)
async def create_task(
    task_data: TaskCreate,
    use_case: CreateTaskUseCase = Depends(get_create_task_use_case)
):
    return await use_case.execute(task_data)

# List tasks endpoint
@router.get(
    "/",
    response_model=ListTasksResponse,
    summary="List Tasks with filtering and cursor-based pagination"
)
async def list_tasks(
    category_id: str | None = Query(None, description="Filter tasks by Category ID"),
    tag_id: str | None = Query(None, description="Filter tasks by Tag ID"),
    cursor: str | None = Query(None, description="Cursor for the next page of results (base64 encoded)"),
    limit: int = Query(10, le=50, description="Max number of items to return"),
    use_case: ListTasksUseCase = Depends(get_list_tasks_use_case)
):
    filter_id = category_id or tag_id
    filter_type = "category" if category_id else ("tag" if tag_id else None)
    return await use_case.execute(filter_type, filter_id, cursor, limit)

# Update task status endpoint
@router.patch(
    "/{task_id}/status",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update the status of a Task"
)
async def update_task_status(
    task_id: str,
    status_update: TaskUpdateStatus,
    use_case: UpdateTaskStatusUseCase = Depends(get_update_status_use_case)
):
    await use_case.execute(task_id, status_update)

# Delete task endpoint
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft delete a Task"
)
async def delete_task(
    task_id: str,
    use_case: DeleteTaskUseCase = Depends(get_delete_task_use_case)
):
    await use_case.execute(task_id)
