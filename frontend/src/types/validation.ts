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

// Export all schemas
export {
  LoginFormSchema,
  SignupFormSchema,
  TaskFormSchema
};