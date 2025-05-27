from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid
from fastapi_mcp import FastApiMCP
from fastapi.middleware.cors import CORSMiddleware
from app.config import Config


# Improved API metadata
app = FastAPI(
    title="Ideas API",
    description="A simple API for managing ideas with CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.router.redirect_slashes = False

mcp = FastApiMCP(app)
mcp.mount()

# MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(Config.MONGODB_URI)
    app.mongodb = app.mongodb_client[Config.MONGODB_DBNAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Pydantic models
class IdeaBase(BaseModel):
    title: str = Field(..., description="The title of the idea", example="Creando un mcp conectado con mongodb y fastapi")
    description: Optional[str] = Field(None, description="Detailed description of the idea", example="guión nuevo para redes sociales")
    status: str = Field(..., description="The status of the idea", example="pending")
    priority: Optional[str] = Field(None, description="The priority of the idea", example="high")

class IdeaCreate(IdeaBase):
    pass

class IdeaUpdate(IdeaBase):
    id: str = Field(..., description="The unique identifier of the idea", example="61b1e2c9-a9c1-4a2d-b3d2-c3d4d5e6f7g8")

class Idea(IdeaBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the idea")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the idea was created")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "61b1e2c9-a9c1-4a2d-b3d2-c3d4d5e6f7g8",
                "title": "Creando un mcp conectado con mongodb y fastapi",
                "description": "guión nuevo para redes sociales",
                "status": "pending",
                "priority": "alta",
                "created_at": "2023-03-01T12:00:00"
            }
        }

#Root endpoint for CRUD operations
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns basic API information and available endpoints.
    """

    return {
        "title": "Ideas API",
        "description": "A simple API for managing ideas with CRUD operations",
        "version": "1.0.0",
        "endpoints": {
            "create_idea": "POST /ideas/",
            "get_ideas": "GET /ideas/",
            "get_idea": "GET /ideas/{idea_id}",
            "update_idea": "PUT /ideas/{idea_id}",
            "delete_idea": "DELETE /ideas/{idea_id}"
        }
    }

@app.get(
        "/ideas/",
        response_model=List[Idea],
        summary="Get all ideas",
        description="Get all ideas.",
        tags=["Ideas"])
async def get_ideas():
    """
    Get all ideas.
    """
    ideas = await app.mongodb.ideas.find().to_list(length=100)
    return ideas

@app.get(
        "/ideas/{idea_id}",
        response_model=Idea,
        summary="Get a specific idea by its ID",
        description="Get a specific idea by its ID.",
        status_code=status.HTTP_200_OK,
        tags=["Ideas"])
async def get_idea(idea_id: str):
    """
    Get a specific idea by its ID.
    """
    idea = await app.mongodb["ideas"].find_one({"id": idea_id})
    if not idea or idea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Idea with id {idea_id} not found"
        )
    return idea

@app.post(
        "/ideas/",
        response_model=Idea,
        status_code=status.HTTP_201_CREATED,
        tags=["Ideas"],
        summary="Create a new idea",
        description="Create a new idea with the provided details."
)
async def create_idea(idea: IdeaCreate):
    """
    Create a new idea.
    """
    try:
        print(idea)
        new_idea = Idea(
            title=idea.title,
            description=idea.description if idea.description else "alta",
            status=idea.status,
            priority=idea.priority,
            created_at=datetime.now()
        )
        
        await app.mongodb["ideas"].insert_one(new_idea.model_dump())
        return new_idea
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating idea: {e}"
        )

@app.put(
        "/ideas/{idea_id}",
        response_model=Idea,
        summary="Update an existing idea",
        description="Update an existing idea with the provided details.",
        tags=["Ideas"],
        status_code=200
        )
async def update_idea(idea_id: str, idea: IdeaUpdate):
    """
    Update an existing idea.
    """
    update_results = await app.mongodb["ideas"].update_one(
        {"id": idea_id},
        {"$set": idea.model_dump()}
    )

    if update_results.modified_count == 0:
        ideas_exists = app.mongodb["ideas"].find_one({"id": idea_id})
        if not ideas_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Idea with id {idea_id} not found"
            )
    
    updated_idea = await app.mongodb["ideas"].find_one({"id": idea_id})
    return updated_idea

@app.put(
        "/ideas/change_status/{idea_id}",
        response_model=Idea,
        summary="Change the status of an existing idea",
        description="Change the status of an existing idea with the provided details.",
        tags=["Ideas"],
        status_code=200
        )
async def change_status_idea(idea_id: str, idea: IdeaUpdate):
    """
    Change the status of an existing idea.
    """
    update_results = await app.mongodb["ideas"].update_one(
        {"id": idea_id},
        {"$set": {"status": idea.status}}
    )

    if update_results.modified_count == 0:
        ideas_exists = app.mongodb["ideas"].find_one({"id": idea_id})
        if not ideas_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Idea with id {idea_id} not found"
            )
    
    updated_idea = await app.mongodb["ideas"].find_one({"id": idea_id})
    return updated_idea

@app.delete(
        "/ideas/{idea_id}",
        summary="Delete an existing idea",
        description="Delete an existing idea with the provided id.",
        tags=["Ideas"],
        status_code=status.HTTP_204_NO_CONTENT
        )
async def delete_idea(idea_id: str):
    """
    Delete an existing idea.
    """
    deleted_results = await app.mongodb["ideas"].delete_one({"id": idea_id})
    if deleted_results.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Idea with id {idea_id} not found"
        )

    return None

mcp.setup_server()