# Frontend Authentication System

This is the frontend application for the Todo Full Stack application, built with Next.js 16+, React 18, TypeScript, and Tailwind CSS. It implements a complete authentication system with user registration, login, and protected dashboard access.

## Features

- User registration and login
- Protected routes with authentication
- Task management system
- Responsive design with Tailwind CSS
- JWT-based authentication
- Form validation with Zod and React Hook Form
- API client with automatic token refresh

## Tech Stack

- Next.js 16+ with App Router
- React 18
- TypeScript 5+
- Tailwind CSS
- Better Auth
- Zod for validation
- React Hook Form
- Shadcn UI components

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── (auth)/          # Authentication pages (login, signup)
│   │   │   ├── login/
│   │   │   └── signup/
│   │   ├── dashboard/       # Protected dashboard route
│   │   ├── globals.css      # Global styles
│   │   └── layout.tsx       # Root layout
│   ├── components/          # Reusable UI components
│   │   ├── ui/              # Base UI components (Shadcn)
│   │   ├── auth/            # Authentication-related components
│   │   ├── dashboard/       # Dashboard components (TaskCard, TaskForm)
│   │   └── navbar/          # Navigation bar component
│   ├── lib/                 # Utility functions and services
│   │   ├── auth/            # Authentication utilities
│   │   ├── api/             # API client with JWT handling
│   │   └── utils/           # General utilities
│   └── types/               # TypeScript type definitions
├── public/                  # Static assets
├── .env.local               # Environment variables (JWT secret, API URLs)
├── next.config.js           # Next.js configuration
├── tailwind.config.js       # Tailwind CSS configuration
└── tsconfig.json            # TypeScript configuration
```

## API Client Usage

The application uses a custom API client located at `src/lib/api/client.ts` that handles JWT authentication and token refresh automatically.

### Example Usage:

```typescript
import apiClient from '@/lib/api/client';

// GET request
const response = await apiClient.get('/api/tasks');

// POST request
const response = await apiClient.post('/api/tasks', {
  title: 'New Task',
  description: 'Task description',
  status: 'todo'
});

// PUT request
const response = await apiClient.put(`/api/tasks/${taskId}`, {
  title: 'Updated Task',
  status: 'in-progress'
});

// DELETE request
const response = await apiClient.delete(`/api/tasks/${taskId}`);
```

The API client automatically:
- Adds the Authorization header with the JWT token
- Handles token refresh when receiving a 401 response
- Redirects to login if token refresh fails
- Returns standardized response objects

## Environment Variables

Copy `.env.local.example` to `.env.local` and update the values:

```
# Backend API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BASE_URL=http://localhost:3000

# Better Auth Configuration
AUTH_SECRET=your_auth_secret_here
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_URL=http://localhost:3000

# Database Configuration (if needed)
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db

# JWT Configuration
JWT_SECRET=your_jwt_secret_here
JWT_EXPIRES_IN=24h
```

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Visit `http://localhost:3000` in your browser.

## Authentication Flow

1. Users can register at `/signup` or login at `/login`
2. Successful authentication stores session data in localStorage
3. Protected routes are wrapped with `ProtectedRoute` component
4. API requests automatically include the JWT token in the Authorization header
5. Token refresh happens automatically when receiving a 401 response

## Components

- `AuthProvider` and `useAuth` hook: Manages authentication state
- `ProtectedRoute`: Wraps protected pages/components
- `TaskCard`: Displays individual tasks
- `TaskForm`: Handles task creation and editing
- `Navbar`: Navigation bar with user profile and logout
