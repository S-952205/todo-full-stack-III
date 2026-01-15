# Data Models: Frontend Authentication System

## Frontend-Specific Data Models

### User Session Model
Represents the authenticated user session state in the frontend application.

```typescript
interface UserSession {
  id: string;           // Unique identifier for the user session
  userId: string;       // Reference to the user ID from authentication
  email: string;        // User's email address
  name?: string;        // Optional user name
  accessToken: string;  // JWT access token
  refreshToken?: string; // Optional refresh token
  expiresAt: Date;      // Token expiration time
  createdAt: Date;      // Session creation time
  updatedAt: Date;      // Last session update time
}
```

### Authentication State Model
Manages the authentication state in the frontend application.

```typescript
interface AuthState {
  isAuthenticated: boolean;
  user: UserSession | null;
  isLoading: boolean;
  error: string | null;
}
```

### API Response Models
Standardized response structures for API communication.

```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    pageSize: number;
    totalCount: number;
    totalPages: number;
  };
}
```

### Task Model (Frontend Representation)
Frontend representation of the task entity, compatible with backend model.

```typescript
interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'todo' | 'in-progress' | 'done';
  userId: string;       // Owner of the task
  createdAt: Date;
  updatedAt: Date;
  dueDate?: Date;
}
```

### Form Data Models
Data structures for form handling and validation.

```typescript
interface LoginForm {
  email: string;
  password: string;
}

interface SignupForm extends LoginForm {
  name?: string;
}

interface TaskForm {
  title: string;
  description?: string;
  status: 'todo' | 'in-progress' | 'done';
  dueDate?: Date;
}
```

## State Management Models

### Task Management State
State structure for managing tasks in the frontend.

```typescript
interface TaskState {
  tasks: Task[];
  filteredTasks: Task[];
  loading: boolean;
  error: string | null;
  selectedTask: Task | null;
  filters: {
    status?: 'todo' | 'in-progress' | 'done';
    searchTerm?: string;
  };
}
```

## Validation Models

### Input Validation Schema
Zod schema definitions for form validation.

```typescript
import { z } from 'zod';

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const LoginFormSchema = z.object({
  email: z.string().regex(emailRegex, 'Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export const SignupFormSchema = LoginFormSchema.extend({
  name: z.string().min(1, 'Name is required').max(100),
});

export const TaskFormSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200),
  description: z.string().max(1000).optional(),
  status: z.enum(['todo', 'in-progress', 'done']),
  dueDate: z.coerce.date().optional(),
});
```

## API Client Configuration Model

### API Client Settings
Configuration for the unified API client.

```typescript
interface ApiClientConfig {
  baseUrl: string;
  defaultHeaders: Record<string, string>;
  timeout: number;
  retries: number;
}
```

## Security Models

### Token Security Model
Structure for managing security tokens safely.

```typescript
interface SecureToken {
  value: string;
  type: 'access' | 'refresh';
  expiresAt: Date;
  isValid(): boolean;
  isExpired(): boolean;
  willExpireSoon(minutes?: number): boolean;
}
```