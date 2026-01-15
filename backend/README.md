# Todo Backend API

A secure FastAPI backend for managing Todo tasks with Neon PostgreSQL database integration and JWT authentication.

## Features

- **JWT Authentication**: All endpoints require valid JWT tokens
- **User Isolation**: Users can only access their own tasks
- **Full CRUD Operations**: Create, Read, Update, Delete tasks
- **Task Management**: Title, description, completion status, timestamps
- **Secure API**: Proper validation and error handling

## API Endpoints

All endpoints are under `/api/v1/` prefix:

- `POST /tasks` - Create a new task
- `GET /tasks` - Get all tasks for authenticated user
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task details
- `PATCH /tasks/{id}/complete` - Toggle completion status
- `DELETE /tasks/{id}` - Delete task

## Requirements

- Python 3.13+
- uv package manager

## Setup

1. **Create virtual environment and install dependencies:**
```bash
cd backend
uv venv --python 3.13
source .venv/bin/activate
uv add fastapi sqlmodel psycopg2-binary python-jose uvicorn python-multipart pydantic pydantic-settings httpx pytest
```

2. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your database URL and auth secret
```

3. **Run the application:**
```bash
uv run uvicorn main:app --reload --port 8000
```

The database tables will be automatically created on application startup.

## Testing

Run the test suite:
```bash
uv run python -m pytest tests/ -v
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## Security

- All endpoints require `Authorization: Bearer <token>` header
- User ID from JWT is validated against task ownership
- Input validation for all fields (title max 200 chars)
- Proper error responses with appropriate HTTP status codes