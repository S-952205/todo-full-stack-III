# Quickstart Guide: Todo Backend & Database (Phase 1)

## Prerequisites
- Python 3.13+
- Access to Neon PostgreSQL database
- Better Auth secret key

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Create virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your DATABASE_URL and BETTER_AUTH_SECRET
   ```

5. **Start the development server**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**
   - API endpoints: http://localhost:8000/api/v1/
   - Documentation: http://localhost:8000/docs

## Environment Variables
- `DATABASE_URL`: Connection string for Neon PostgreSQL database
- `BETTER_AUTH_SECRET`: Secret key for JWT verification

## Testing
Run the tests with pytest:
```bash
pytest
```

## API Usage
All API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

The API follows REST conventions with the base path `/api/v1/`.