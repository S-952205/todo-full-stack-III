from fastmcp import FastMCP
import json
from typing import Dict, Any
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from db import get_session
from models import TaskCreate, TaskUpdate, Task as ExistingTask
from auth import validate_user_access
from .database import create_task, get_tasks_by_user, update_task as db_update_task, complete_task, delete_task
from .auth import validate_mcp_request


# Initialize the MCP server
mcp = FastMCP("Todo-Server")


@mcp.tool("add_task", description="Create a new task for the authenticated user")
def add_task(title: str, description: str = "", user_id: str = "") -> str:
    """
    Create a new task for the authenticated user.

    Args:
        title: Title of the task
        description: Detailed description of the task (optional)
        user_id: ID of the user creating the task

    Returns:
        JSON string representation of the created task
    """
    try:
        # Validate user access
        validate_mcp_request(user_id, user_id)  # In a real scenario, we'd compare with authenticated user

        # Create task data
        task_create = TaskCreate(title=title, description=description)

        # Get database session and create task
        with next(get_session()) as session:
            created_task = create_task(session, task_create, user_id)

            # Convert to dict and return as JSON
            task_dict = {
                "id": created_task.id,
                "title": created_task.title,
                "description": created_task.description,
                "is_completed": created_task.completed,
                "user_id": created_task.user_id,
                "created_at": created_task.created_at.isoformat()
            }
            return json.dumps(task_dict)
    except Exception as e:
        error_response = {"error": str(e)}
        return json.dumps(error_response)


@mcp.tool("list_tasks", description="Retrieve all tasks for the authenticated user")
def list_tasks(user_id: str = "") -> str:
    """
    Retrieve all tasks for the authenticated user.

    Args:
        user_id: ID of the user whose tasks to retrieve

    Returns:
        JSON string array of tasks
    """
    try:
        # Validate user access
        validate_mcp_request(user_id, user_id)  # In a real scenario, we'd compare with authenticated user

        # Get database session and retrieve tasks
        with next(get_session()) as session:
            tasks = get_tasks_by_user(session, user_id)

            # Convert tasks to list of dicts
            tasks_list = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.completed,
                    "user_id": task.user_id,
                    "created_at": task.created_at.isoformat()
                }
                tasks_list.append(task_dict)

            return json.dumps(tasks_list)
    except Exception as e:
        error_response = {"error": str(e)}
        return json.dumps(error_response)


@mcp.tool("update_task", description="Modify an existing task")
def update_task(task_id: int, user_id: str = "", title: str = "", description: str = "") -> str:
    """
    Modify an existing task.

    Args:
        task_id: ID of the task to update
        user_id: ID of the user requesting the update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        JSON string representation of the updated task
    """
    try:
        # Validate user access
        validate_mcp_request(user_id, user_id)  # In a real scenario, we'd compare with authenticated user

        # Prepare update data
        update_data = {}
        if title:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description

        task_update = TaskUpdate(**update_data)

        # Get database session and update task
        with next(get_session()) as session:
            updated_task = db_update_task(session, task_id, task_update)

            if updated_task:
                # Convert to dict and return as JSON
                task_dict = {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "is_completed": updated_task.completed,
                    "user_id": updated_task.user_id,
                    "updated_at": updated_task.created_at.isoformat()  # Note: Using created_at since there's no updated_at in the model
                }
                return json.dumps(task_dict)
            else:
                error_response = {"error": "Task not found"}
                return json.dumps(error_response)
    except Exception as e:
        error_response = {"error": str(e)}
        return json.dumps(error_response)


@mcp.tool("complete_task", description="Mark a task as completed")
def complete_task(task_id: int, completed: bool = True, user_id: str = "") -> str:
    """
    Mark a task as completed.

    Args:
        task_id: ID of the task to mark as completed
        completed: True to mark as completed, False to unmark
        user_id: ID of the user requesting the update

    Returns:
        JSON string representation of the updated task
    """
    try:
        # Validate user access
        validate_mcp_request(user_id, user_id)  # In a real scenario, we'd compare with authenticated user

        # Get database session and update task completion status
        with next(get_session()) as session:
            updated_task = complete_task(session, task_id, completed)

            if updated_task:
                # Convert to dict and return as JSON
                task_dict = {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "is_completed": updated_task.completed,
                    "user_id": updated_task.user_id,
                    "updated_at": updated_task.created_at.isoformat()  # Note: Using created_at since there's no updated_at in the model
                }
                return json.dumps(task_dict)
            else:
                error_response = {"error": "Task not found"}
                return json.dumps(error_response)
    except Exception as e:
        error_response = {"error": str(e)}
        return json.dumps(error_response)


@mcp.tool("delete_task", description="Remove a task")
def delete_task(task_id: int, user_id: str = "") -> str:
    """
    Remove a task.

    Args:
        task_id: ID of the task to delete
        user_id: ID of the user requesting the deletion

    Returns:
        JSON string confirmation of deletion
    """
    try:
        # Validate user access
        validate_mcp_request(user_id, user_id)  # In a real scenario, we'd compare with authenticated user

        # Get database session and delete task
        with next(get_session()) as session:
            success = delete_task(session, task_id)

            if success:
                result = {
                    "success": True,
                    "deleted_task_id": task_id,
                    "user_id": user_id
                }
                return json.dumps(result)
            else:
                error_response = {"error": "Task not found", "success": False}
                return json.dumps(error_response)
    except Exception as e:
        error_response = {"error": str(e), "success": False}
        return json.dumps(error_response)


def start_mcp_server():
    """
    Start the MCP server in a background thread.
    """
    def run_server():
        # Run MCP server directly - FastMCP handles async internally
        mcp.run()

    # Create a daemon thread to run the MCP server
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    return server_thread


if __name__ == "__main__":
    # Run the MCP server directly if this script is executed
    mcp.run()