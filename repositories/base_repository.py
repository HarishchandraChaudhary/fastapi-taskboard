from typing import List, TypeVar, Generic, Type, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from schemas.base import BaseMongoModel

# Type variable for Pydantic model
T = TypeVar('T', bound=BaseMongoModel)

class BaseRepository(Generic[T]):
    """
    Generic base class for MongoDB repositories.
    Provides fundamental CRUD operations using motor.
    """
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, model: Type[T]):
        self.collection = db[collection_name]
        self.model = model

    async def create(self, data: Dict[str, Any]) -> T:
        """Creates a new document in the collection, adding timestamps."""
        now = datetime.now()
        data.update({"created_at": now, "updated_at": now})
        
        result = await self.collection.insert_one(data)
        document = await self.collection.find_one({"_id": result.inserted_id})
        
        # Validate the retrieved document against the Pydantic model
        return self.model.model_validate(document)

    async def get_by_id(self, id: str) -> Optional[Dict]:
        """Retrieves a single document by its ObjectId string."""
        if not ObjectId.is_valid(id):
            return None
        return await self.collection.find_one({"_id": ObjectId(id)})

    async def get_all(self) -> List[Dict]:
        """Retrieves all documents from the collection."""
        return await self.collection.find().to_list(None)

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict]:
        """Updates an existing document and sets the updated_at field."""
        if not ObjectId.is_valid(id):
            return None
        
        # Ensure 'updated_at' is always current
        update_data = {"$set": {**data, "updated_at": datetime.now()}}
        
        await self.collection.update_one(
            {"_id": ObjectId(id)},
            update_data
        )
        # Fetch the updated document to return
        return await self.get_by_id(id)

    async def delete(self, id: str) -> bool:
        """Deletes a document by its ID."""
        if not ObjectId.is_valid(id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
