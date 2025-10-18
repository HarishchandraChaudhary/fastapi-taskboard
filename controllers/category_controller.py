from fastapi import APIRouter, status
from schemas.category import CategoryCreate, CategoryResponse
from use_cases.category_tag import CreateCategoryUseCase
from .base import ContainerDep

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Category"
)
async def create_category(
    category_data: CategoryCreate,
    container: ContainerDep
):
    use_case = container.resolve(CreateCategoryUseCase)
    return await use_case.execute(category_data)