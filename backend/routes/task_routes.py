from fastapi import APIRouter, HTTPException, status, Depends
from models import TaskCreate, TaskUpdate, TaskResponse
from database import tasks_collection
from auth import get_current_user
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


def task_doc_to_response(task: dict) -> TaskResponse:
    """Convert a MongoDB task document to a TaskResponse model."""
    return TaskResponse(
        id=str(task["_id"]),
        title=task["title"],
        description=task.get("description", ""),
        status=task["status"],
        due_date=task.get("due_date"),
        created_at=task["created_at"],
        updated_at=task["updated_at"],
        user_id=task["user_id"],
    )


@router.get("")
async def get_tasks(current_user: dict = Depends(get_current_user)):
    """Get all tasks for the authenticated user."""
    cursor = tasks_collection.find({"user_id": current_user["id"]}).sort(
        "created_at", -1
    )
    tasks = []
    async for task in cursor:
        tasks.append(task_doc_to_response(task))
    return {"tasks": tasks}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate, current_user: dict = Depends(get_current_user)
):
    """Create a new task for the authenticated user."""
    now = datetime.now(timezone.utc).isoformat()

    task_doc = {
        "title": task_data.title,
        "description": task_data.description or "",
        "status": task_data.status.value,
        "due_date": task_data.due_date,
        "user_id": current_user["id"],
        "created_at": now,
        "updated_at": now,
    }

    result = await tasks_collection.insert_one(task_doc)
    task_doc["_id"] = result.inserted_id

    return {"message": "Task created successfully", "task": task_doc_to_response(task_doc)}


@router.put("/{task_id}")
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update an existing task. Only the task owner can update."""
    # Validate ObjectId
    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid task ID"
        )

    # Find the task and verify ownership
    task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    if task["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task",
        )

    # Build update document with only provided fields
    update_fields = {}
    if task_data.title is not None:
        update_fields["title"] = task_data.title
    if task_data.description is not None:
        update_fields["description"] = task_data.description
    if task_data.status is not None:
        update_fields["status"] = task_data.status.value
    if task_data.due_date is not None:
        update_fields["due_date"] = task_data.due_date

    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

    await tasks_collection.update_one(
        {"_id": ObjectId(task_id)}, {"$set": update_fields}
    )

    updated_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    return {
        "message": "Task updated successfully",
        "task": task_doc_to_response(updated_task),
    }


@router.delete("/{task_id}")
async def delete_task(
    task_id: str, current_user: dict = Depends(get_current_user)
):
    """Delete a task. Only the task owner can delete."""
    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid task ID"
        )

    task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    if task["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task",
        )

    await tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return {"message": "Task deleted successfully"}
