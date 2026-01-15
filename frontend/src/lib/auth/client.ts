import { createAuthClient } from 'better-auth/react';
import { useAuth } from '@/context/auth-context';

// Initialize Better Auth client
const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
  fetchOptions: {
    // Custom fetch options if needed
  },
});

// Export the auth client instance
export { authClient };

// Additional helper functions for authentication
export const getAuthHeaders = (): { Authorization?: string } => {
  if (typeof window !== 'undefined') {
    const storedSession = localStorage.getItem('userSession');
    if (storedSession) {
      try {
        const session = JSON.parse(storedSession);
        return {
          Authorization: `Bearer ${session.accessToken}`,
        };
      } catch (error) {
        console.error('Error getting auth headers:', error);
        return {};
      }
    }
  }
  return {};
};

// Function to check if user is authenticated
export const isAuthenticated = (): boolean => {
  if (typeof window !== 'undefined') {
    const storedSession = localStorage.getItem('userSession');
    if (storedSession) {
      try {
        const session = JSON.parse(storedSession);
        // Check if token is still valid (not expired)
        const expiresAt = new Date(session.expiresAt);
        return expiresAt > new Date();
      } catch (error) {
        console.error('Error checking authentication:', error);
        return false;
      }
    }
  }
  return false;
};