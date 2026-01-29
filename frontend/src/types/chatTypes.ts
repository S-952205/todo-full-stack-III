// Types for the chat functionality

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface Conversation {
  id: string;
  title: string;
  userId: string;
  createdAt: string;
  updatedAt: string;
  status: 'active' | 'archived' | 'deleted';
}

export interface ChatRequest {
  message: string;
  conversationId: string;
  userId: string;
}

export interface ChatResponse {
  success: boolean;
  response: string;
  conversationId: string;
  toolResult?: string;
  error?: string;
}

export interface ToolResult {
  success: boolean;
  data?: any;
  error?: string;
  message?: string;
}