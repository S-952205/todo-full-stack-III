# Todo Full Stack Application

A complete full-stack todo application with authentication, built using modern technologies. The application features a Next.js 16+ frontend with TypeScript and Tailwind CSS, and a FastAPI backend with PostgreSQL database integration.

## 🚀 Features

- **Full Authentication System**: User registration, login, and session management
- **Task Management**: Create, read, update, and delete tasks
- **User Isolation**: Users can only access their own tasks
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode Support**: Automatic dark/light mode with toggle functionality
- **Secure API**: JWT-based authentication and authorization
- **Modern UI**: Built with Shadcn UI components

## 🌐 Live Deployments

- **Frontend**: [Todo App Frontend (Vercel)](https://frontend-beta-teal-20.vercel.app)
- **Backend**: [Todo App Backend (Hugging Face)](https://sufyanalisyed-todo-full-stack.hf.space)

Try out the application live! The frontend is hosted on Vercel and the backend API is deployed on Hugging Face.

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS v4 with custom theme
- **Authentication**: Better Auth
- **Forms**: React Hook Form with Zod validation
- **UI Components**: Shadcn UI
- **Package Manager**: npm

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLModel
- **Authentication**: JWT tokens
- **Package Manager**: uv

## 📁 Project Structure

```
todo-full-stack/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application entry point
│   ├── models.py           # Database models
│   ├── auth.py             # Authentication logic
│   ├── db.py               # Database connection and setup
│   ├── routes/             # API route handlers
│   ├── config.py           # Configuration settings
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/            # Application pages and routes
│   │   ├── components/     # Reusable UI components
│   │   ├── lib/            # Utilities and API clients
│   │   └── types/          # TypeScript type definitions
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.ts  # Tailwind CSS configuration
└── README.md               # This file
```

## 🏃‍♂️ Getting Started

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.13+ (for backend)
- uv package manager (for backend)
- PostgreSQL database (Neon recommended)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment and install dependencies:
   ```bash
   uv venv --python 3.13
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and auth secret
   ```

4. Run the application:
   ```bash
   uv run uvicorn main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your API URLs and auth settings
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Visit `http://localhost:3000` in your browser.

## 🌐 API Endpoints

The backend provides a secure API under `/api/v1/`:

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /tasks` - Create a new task
- `GET /tasks` - Get all tasks for authenticated user
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task details
- `PATCH /tasks/{id}/complete` - Toggle completion status
- `DELETE /tasks/{id}` - Delete task

All endpoints (except auth) require `Authorization: Bearer <token>` header.

## 🔐 Authentication Flow

1. Users register or login via the frontend
2. Successful authentication returns JWT tokens
3. Tokens are stored in localStorage and sent with API requests
4. Backend validates tokens and enforces user isolation
5. Frontend automatically refreshes expired tokens

## 🧪 Testing

### Backend Tests
```bash
cd backend
uv run python -m pytest tests/ -v
```

### Frontend Development
The frontend includes form validation and error handling for all user interactions.

## 🎨 UI Features

- **Dark/Light Mode**: Automatic system preference detection with manual toggle
- **Responsive Layout**: Mobile-first design that works on all screen sizes
- **Form Validation**: Client-side validation with user-friendly error messages
- **Loading States**: Visual feedback during API requests
- **Error Handling**: Graceful error display and recovery

## 🚀 Deployment

### Backend
- Set environment variables for production
- Deploy to a Python-compatible hosting service (e.g., Railway, Heroku, AWS)
- Ensure PostgreSQL database is configured for production

### Frontend
- Build for production: `npm run build`
- Serve the built application (e.g., Vercel, Netlify, AWS S3)
- Configure environment variables for production API URLs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Issues

If you encounter any issues, please open an issue in the repository with detailed information about the problem and steps to reproduce.