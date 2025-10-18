from repositories.task_repository import TaskRepository
from schemas.category import CategoryCreate, CategoryResponse
from entities.task import Category, Tag
from schemas.category import TagCreate, TagResponse

class CreateCategoryUseCase:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def execute(self, category_data: CategoryCreate) -> CategoryResponse:
        category_entity = Category(**category_data.model_dump())
        created_category = await self.task_repo.create_category(category_entity)
        return CategoryResponse.model_validate(created_category)

class CreateTagUseCase:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def execute(self, tag_data: TagCreate) -> TagResponse:
        tag_entity = Tag(**tag_data.model_dump())
        created_tag = await self.task_repo.create_tag(tag_entity)
        return TagResponse.model_validate(created_tag)