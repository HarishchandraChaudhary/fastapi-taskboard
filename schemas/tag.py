from typing import Optional
from pydantic import BaseModel, Field
# FIX: Changed to absolute import to reliably locate BaseSchema from the project root
from schemas.base import BaseSchema

# --- Base Schema ---

class TagBase(BaseModel):
    """Base schema for tags, containing common fields."""
    name: str = Field(..., max_length=50, description="The name of the tag.")
    
    class Config:
        # Allows fields to be accessed as tag.name instead of tag['name']
        from_attributes = True

# --- Input Schemas ---

class TagCreate(TagBase):
    """Schema for creating a new tag."""
    # No extra fields needed, inherits 'name' from TagBase

class TagUpdate(TagBase):
    """Schema for updating an existing tag. All fields are optional."""
    name: Optional[str] = Field(None, max_length=50, description="The new name of the tag.")

# --- Output Schemas ---

class TagRead(TagBase, BaseSchema):
    """Schema for reading a tag, includes BaseSchema fields (id, timestamps)."""
    # Inherits 'name' from TagBase and ID/timestamps from BaseSchema
    pass
