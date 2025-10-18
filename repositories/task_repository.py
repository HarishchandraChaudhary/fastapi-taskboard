from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import Optional
import base64

from entities.task import Task, TaskStatus, Category, Tag

# Helper function for safe ID conversion
def to_object_id(id_str: str) -> Optional[ObjectId]:
    try:
        return ObjectId(id_str)
    except:
        return None

class TaskRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.tasks = db.tasks
        self.categories = db.categories
        self.tags = db.tags
        self.tasks_categories = db.tasks_categories
        self.tasks_tags = db.tasks_tags

    # --- Task Operations ---

    async def create_task(self, task: Task, category_ids: list[str], tag_ids: list[str]) -> Task:
        """Creates a task and its associated relationships."""
        
        data_to_insert = {k: v for k, v in task.__dict__.items() if v is not None and k != 'id'}
        data_to_insert["_id"] = ObjectId()
        
        result = await self.tasks.insert_one(data_to_insert)
        task.id = str(result.inserted_id)

        # Create relationships
        if category_ids:
            # Only proceed with valid category IDs
            valid_category_ids = [c_id for c_id in category_ids if to_object_id(c_id)]
            category_relationships = [
                {"task_id": task.id, "category_id": c_id}
                for c_id in valid_category_ids
            ]
            if category_relationships:
                await self.tasks_categories.insert_many(category_relationships)
        
        if tag_ids:
            # Only proceed with valid tag IDs
            valid_tag_ids = [t_id for t_id in tag_ids if to_object_id(t_id)]
            tag_relationships = [
                {"task_id": task.id, "tag_id": t_id}
                for t_id in valid_tag_ids
            ]
            if tag_relationships:
                await self.tasks_tags.insert_many(tag_relationships)

        return task

    async def update_task_status(self, task_id: str, new_status: TaskStatus) -> bool:
        """Updates the status of a task."""
        object_task_id = to_object_id(task_id)
        if not object_task_id:
            return False

        result = await self.tasks.update_one(
            {"_id": object_task_id, "deleted": False},
            {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count == 1
    
    async def soft_delete_task(self, task_id: str) -> bool:
        """Performs a soft delete on a task."""
        object_task_id = to_object_id(task_id)
        if not object_task_id:
            return False

        result = await self.tasks.update_one(
            {"_id": object_task_id, "deleted": False},
            {"$set": {"deleted": True, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count == 1
    
    # --- Relationship Lookups ---

    async def get_task_categories(self, task_id: str) -> list[Category]:
        """Finds categories for a given task ID using the relationship collection."""
        
        pipeline = [
            {"$match": {"task_id": task_id}},
            {"$lookup": {
                "from": "categories",
                "localField": "category_id",
                "foreignField": "_id",
                "as": "category_info"
            }},
            {"$unwind": "$category_info"},
            {"$replaceRoot": {"newRoot": "$category_info"}}
        ]
        
        categories = []
        # Use aggregate on the relationship collection, not the main tasks collection
        async for doc in self.tasks_categories.aggregate(pipeline):
            categories.append(self._document_to_category(doc))
        return categories

    async def get_task_tags(self, task_id: str) -> list[Tag]:
        """Finds tags for a given task ID using the relationship collection."""
        
        pipeline = [
            {"$match": {"task_id": task_id}},
            {"$lookup": {
                "from": "tags",
                "localField": "tag_id",
                "foreignField": "_id",
                "as": "tag_info"
            }},
            {"$unwind": "$tag_info"},
            {"$replaceRoot": {"newRoot": "$tag_info"}}
        ]
        
        tags = []
        async for doc in self.tasks_tags.aggregate(pipeline):
            tags.append(self._document_to_tag(doc))
        return tags


    # --- List Tasks (Filtering and Cursor Pagination) ---

    async def list_tasks(self, filter_id: str | None, filter_type: str | None, cursor: str | None, limit: int = 10):
        """Lists tasks with filtering and cursor pagination."""
        base_query = {"deleted": False}
        
        # 1. Handle Filtering by Category/Tag
        if filter_id and filter_type in ["category", "tag"]:
            rel_collection = self.tasks_categories if filter_type == "category" else self.tasks_tags
            rel_field = "category_id" if filter_type == "category" else "tag_id"
            
            task_ids_to_filter = set()
            # Find all task_ids related to the filter_id
            async for rel in rel_collection.find({rel_field: filter_id}, {"task_id": 1}):
                task_ids_to_filter.add(rel["task_id"])
            
            if not task_ids_to_filter:
                return [], None # No tasks match the filter

            # Ensure the task_ids are converted to ObjectIds for the main query
            valid_object_ids = [to_object_id(tid) for tid in task_ids_to_filter if to_object_id(tid)]
            base_query["_id"] = {"$in": valid_object_ids}

        # 2. Handle Cursor Pagination
        if cursor:
            try:
                decoded_cursor = base64.b64decode(cursor).decode('utf-8')
                last_id = ObjectId(decoded_cursor)
                
                # Update the _id query to include the cursor condition ($gt)
                if "_id" in base_query and isinstance(base_query["_id"], dict):
                    base_query["_id"].update({"$gt": last_id})
                else:
                    base_query["_id"] = {"$gt": last_id}

            except Exception:
                # Invalid cursor, ignore the cursor
                pass

        # 3. Execute Query (limit + 1 for next_cursor check)
        tasks_list = []
        cursor_result = self.tasks.find(base_query).sort("_id", 1).limit(limit + 1)
        
        async for doc in cursor_result:
            tasks_list.append(self._document_to_task(doc))
        
        # 4. Generate next_cursor
        next_cursor = None
        if len(tasks_list) > limit:
            # We fetched one extra item; use its ID for the next cursor
            next_task_doc = tasks_list.pop(limit) # Remove the extra item
            last_id_str = str(tasks_list[-1].id)
            next_cursor = base64.b64encode(last_id_str.encode('utf-8')).decode('utf-8')
        elif tasks_list:
             # If we got exactly 'limit' tasks, we use the last one's ID for the cursor
             # but check the database to see if more exist (simplified here by only returning cursor if > limit)
             # NOTE: For true pagination, we should use the last item ID when results == limit
             # For simplicity, we stick to the limit+1 pattern:
             if len(tasks_list) == limit:
                last_id_str = str(tasks_list[-1].id)
                next_cursor = base64.b64encode(last_id_str.encode('utf-8')).decode('utf-8')
             else:
                next_cursor = None

        return tasks_list, next_cursor


    # --- Category/Tag Operations ---
    async def create_category(self, category: Category) -> Category:
        data_to_insert = {k: v for k, v in category.__dict__.items() if v is not None and k != 'id'}
        data_to_insert["_id"] = ObjectId()
        result = await self.categories.insert_one(data_to_insert)
        category.id = str(result.inserted_id)
        return category

    async def create_tag(self, tag: Tag) -> Tag:
        data_to_insert = {k: v for k, v in tag.__dict__.items() if v is not None and k != 'id'}
        data_to_insert["_id"] = ObjectId()
        result = await self.tags.insert_one(data_to_insert)
        tag.id = str(result.inserted_id)
        return tag

    # --- Private/Helper Methods ---
    def _document_to_task(self, doc: dict) -> Task:
        return Task(
            id=str(doc["_id"]),
            title=doc["title"],
            description=doc["description"],
            due_date=doc["due_date"],
            status=doc["status"],
            deleted=doc["deleted"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )
    
    def _document_to_category(self, doc: dict) -> Category:
        return Category(
            id=str(doc["_id"]),
            name=doc["name"],
            description=doc["description"],
        )
    
    def _document_to_tag(self, doc: dict) -> Tag:
        return Tag(
            id=str(doc["_id"]),
            name=doc["name"],
            description=doc["description"],
        )