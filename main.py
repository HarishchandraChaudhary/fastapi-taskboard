import os
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

# Load env vars
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Setup DB + DI Container
client = AsyncIOMotorClient(MONGO_URL)
database = client[MONGO_DB_NAME]

from container import create_container
global_container = create_container(database)

# ⛔ Don't import controllers BEFORE this override!
from controllers import base
base.get_container = lambda: global_container  # ✅ Override placeholder

# ✅ Now import the controllers
from controllers import task_controller, category_controller, tag_controller

# Create FastAPI app
app = FastAPI(
    title="TaskBoard API",
    version="1.0.0",
)

# Register routers
app.include_router(task_controller.router)
app.include_router(category_controller.router)
app.include_router(tag_controller.router)
