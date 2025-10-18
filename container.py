from punq import Container
from motor.motor_asyncio import AsyncIOMotorDatabase

from repositories.task_repository import TaskRepository
from use_cases.task import (
    CreateTaskUseCase,
    UpdateTaskStatusUseCase,
    DeleteTaskUseCase,
    ListTasksUseCase
)
from use_cases.category_tag import CreateCategoryUseCase, CreateTagUseCase

def create_container(db: AsyncIOMotorDatabase) -> Container:
    container = Container()

    # 1. Database instance (singleton)
    container.register(AsyncIOMotorDatabase, instance=db)

    # 2. Repositories
    container.register(TaskRepository)

    # 3. Use Cases
    container.register(CreateTaskUseCase)
    container.register(UpdateTaskStatusUseCase)
    container.register(DeleteTaskUseCase)
    container.register(ListTasksUseCase)
    container.register(CreateCategoryUseCase)
    container.register(CreateTagUseCase)

    return container
