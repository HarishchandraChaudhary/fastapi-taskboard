from fastapi import APIRouter, status
from schemas.category import TagCreate, TagResponse
from use_cases.category_tag import CreateTagUseCase
from .base import ContainerDep

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post(
    "/",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Tag"
)
async def create_tag(
    tag_data: TagCreate,
    container: ContainerDep
):
    use_case = container.resolve(CreateTagUseCase)
    return await use_case.execute(tag_data)