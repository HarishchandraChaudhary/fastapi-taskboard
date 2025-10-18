FastAPI TaskBoard API

This project is a RESTful API for a task management system (TaskBoard), built using FastAPI, MongoDB (via Motor), and implementing a Clean Architecture pattern with Dependency Injection via Punq.

It serves as the backend for managing tasks, categories (like Kanban columns), and tags.

✨ Features

Task Management: Create, Read, Update, and Delete tasks with status, category, and tag associations.

Categories: Manage organizational columns (e.g., To Do, In Progress, Done).

Tags: Define reusable labels (e.g., Urgent, Design, Backend).

Clean Architecture: Clear separation of concerns into Controllers, Services, and Repositories.

Dependency Injection: Uses Punq for managing service and repository dependencies.

Asynchronous Database Access: Uses Motor for non-blocking MongoDB operations.

Automatic Documentation: Full API documentation available at the /docs endpoint (Swagger UI).

🚀 Getting Started

Prerequisites

You need the following installed on your system:

Python 3.10+ (The project was developed using Python 3.11)

MongoDB Instance (Local or cloud service like MongoDB Atlas)

Local Setup

Clone the Repository:

git clone YOUR_REPOSITORY_URL
cd fastapi-taskboard


Create and Activate Virtual Environment:

python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows (PowerShell or Command Prompt)


Install Dependencies:

pip install -r requirements.txt


Configuration (.env File)

You must create a file named .env in the root directory of the project to store your database connection string and name. This file is ignored by Git (as specified in .gitignore) to protect your credentials.

# .env file content
MONGO_URL="mongodb+srv://<user>:<password>@<cluster>.mongodb.net/"
MONGO_DB_NAME="taskboard_db"


Replace the placeholder values with your actual MongoDB connection details.

🏃 Running the Application

Start the FastAPI server using Uvicorn with the --reload flag for development:

uvicorn main:app --reload


The application will start, and the console should show:

INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)


API Documentation

Once the server is running, you can explore and test all API endpoints using the interactive Swagger UI:

Open in Browser: http://127.0.0.1:8000/docs

🏗️ Architecture Overview

The project follows the principles of Clean Architecture, organizing code into distinct layers to maximize testability and maintainability.

Layer

Responsibility

Imports

Controllers (controllers/)

Handles HTTP requests, input validation, and returns responses.

Imports Services

Services (services/)

Contains core business logic and coordination.

Imports Repositories

Repositories (repositories/)

Handles database access (CRUD operations) and data mapping.

Imports Database Client

Schemas (schemas/)

Defines data structures using Pydantic for input/output validation.

Imports Pydantic

The main.py file initializes the MongoDB client, sets up the Punq container, and injects the dependencies into the Controller routes.
