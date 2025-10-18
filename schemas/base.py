from pydantic import BaseModel
from schemas.base import BaseSchema

class TagCreate(BaseModel):
    name: str

class TagUpdate(BaseModel):
    name: str

class TagRead(BaseSchema):
    name: str
