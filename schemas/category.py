from pydantic import BaseModel, Field, ConfigDict

class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=50)
    description: str = Field(..., max_length=200)

class CategoryResponse(BaseModel):
    id: str
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)

# For simplicity, Tag schemas are the same structure as Category schemas
TagCreate = CategoryCreate
TagResponse = CategoryResponse