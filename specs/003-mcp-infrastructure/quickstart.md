# Quickstart Guide: MCP Infrastructure Foundation

## Overview
This guide explains how to set up and run the MCP (Model Context Protocol) server that exposes task operations as AI-callable tools.

## Prerequisites
- Python 3.13+
- uv package manager
- Access to Neon PostgreSQL database
- Better Auth configured for user authentication

## Installation

1. Install the required dependencies:
```bash
uv add fastmcp
```

2. Update your requirements.txt to include the MCP dependencies:
```txt
fastmcp>=0.1.0
```

## Database Setup

1. Create the new database models by running migrations:
```bash
# Add the new Conversation and Message models to your models directory
# Run the migration to create the new tables
alembic revision --autogenerate -m "Add Conversation and Message models"
alembic upgrade head
```

## Running the MCP Server

The MCP server is integrated into the main FastAPI application and will start automatically when the application starts, running on a background thread.

## Using MCP Tools

Once the server is running, the following tools will be available to AI agents:

- `add_task`: Create a new task for the authenticated user
- `list_tasks`: Retrieve all tasks for the authenticated user
- `update_task`: Modify an existing task
- `complete_task`: Mark a task as completed
- `delete_task`: Remove a task

## Security

- All MCP tools validate the user_id to ensure proper data isolation
- Users can only access their own tasks and conversations
- Authentication is handled through JWT tokens

## Development

To test the MCP server locally:
1. Start the development server: `uv run python -m src.main`
2. Connect an AI agent to the MCP server endpoint
3. Verify that all 5 task operations work correctly with proper user isolation