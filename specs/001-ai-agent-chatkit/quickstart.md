# Quickstart Guide: AI Agent & ChatKit UI Implementation

## Overview
This guide provides a quick overview of how to set up and run the AI Agent & ChatKit UI feature.

## Prerequisites
- Python 3.13+
- Node.js 18+ (for frontend)
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- OpenRouter API key for accessing free models
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install fastapi uvicorn openai python-jose[cryptography] psycopg2-binary sqlmodel better-auth python-multipart

# Create .env file with required environment variables
cat > .env << EOF
OPENROUTER_API_KEY=your_openrouter_api_key_here
DATABASE_URL=postgresql://username:password@host:port/database_name
JWT_SECRET=your_jwt_secret_here
EOF

# Initialize the database
python -c "from src.db.init_db import init_db; init_db()"
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env file for frontend
cat > .env.local << EOF
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
EOF

# Build the application
npm run build
```

### 4. Running the Application

#### Backend (API Server)
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

#### Frontend (Next.js App)
```bash
cd frontend
npm run dev
```

The application will be available at http://localhost:3000

## Configuration

### Environment Variables

#### Backend (.env)
- `OPENROUTER_API_KEY`: API key for OpenRouter to access free models
- `DATABASE_URL`: Connection string for PostgreSQL database
- `JWT_SECRET`: Secret key for JWT token signing
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins (optional)

#### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
- `NEXTAUTH_URL`: Base URL for authentication (optional)

## Key Endpoints

### Backend API
- `POST /api/chat`: Main chat endpoint that handles user messages and returns agent responses
- `GET /api/conversations`: Retrieve user's conversation history
- `GET /api/conversations/{id}/messages`: Get messages for a specific conversation

### Frontend Pages
- `/chat`: Main chat interface with ChatKit UI
- `/chat/{conversationId}`: Specific conversation view

## Development Workflow

### Adding New MCP Tools
1. Create a new tool function in `backend/src/tools/mcp_tools.py`
2. Ensure the function has proper type hints and error handling
3. Register the tool with the agent service
4. Test the tool through the chat interface

### Modifying the Database Schema
1. Update the models in `backend/src/models/`
2. Create a new migration using Alembic (if using migrations)
3. Update the data-model.md documentation
4. Test database operations thoroughly

## Troubleshooting

### Common Issues
- **OpenRouter API Error**: Verify that `OPENROUTER_API_KEY` is set correctly and has sufficient credits
- **Database Connection Error**: Check that `DATABASE_URL` is configured correctly
- **Authentication Error**: Ensure JWT secret is properly set and consistent between services
- **Tool Call Failures**: Check that MCP tools are properly registered and have correct schemas

### Logging
- Backend logs are output to stdout/stderr
- Enable debug logging by setting `LOG_LEVEL=debug` in the backend .env file
- Frontend errors are displayed in browser console

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment Notes
- For production, ensure proper SSL certificates are configured
- Set up proper environment variables for production
- Consider using Docker containers for consistent deployment
- Implement proper monitoring and alerting
- Ensure backup procedures for the database