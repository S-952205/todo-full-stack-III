'use client';

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { AuthState, UserSession } from '@/types';

interface AuthContextType {
  state: AuthState;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  updateUser: (userData: Partial<UserSession>) => void;
}

const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  isLoading: true,
  error: null,
};

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: UserSession }
  | { type: 'LOGIN_ERROR'; payload: string }
  | { type: 'SIGNUP_SUCCESS'; payload: UserSession }
  | { type: 'SIGNUP_ERROR'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'UPDATE_USER'; payload: Partial<UserSession> }
  | { type: 'SET_LOADING'; payload: boolean };

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload,
        isLoading: false,
        error: null,
      };
    case 'LOGIN_ERROR':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        isLoading: false,
        error: action.payload,
      };
    case 'SIGNUP_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload,
        isLoading: false,
        error: null,
      };
    case 'SIGNUP_ERROR':
      return {
        ...state,
        isLoading: false,
        error: action.payload,
      };
    case 'LOGOUT':
      return {
        ...initialState,
        isLoading: false,
      };
    case 'UPDATE_USER':
      return {
        ...state,
        user: state.user ? { ...state.user, ...action.payload } : null,
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    default:
      return state;
  }
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check for existing session on mount
  useEffect(() => {
    const checkSession = async () => {
      try {
        // Check if there's a session in localStorage
        const storedSession = localStorage.getItem('userSession');
        if (storedSession) {
          const session: UserSession = JSON.parse(storedSession);

          // Check if session is still valid
          if (new Date(session.expiresAt) > new Date()) {
            dispatch({ type: 'LOGIN_SUCCESS', payload: session });
          } else {
            // Session expired, remove it
            localStorage.removeItem('userSession');
            dispatch({ type: 'LOGOUT' });
          }
        } else {
          dispatch({ type: 'LOGOUT' });
        }
      } catch (error) {
        console.error('Error checking session:', error);
        dispatch({ type: 'LOGOUT' });
      } finally {
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    checkSession();
  }, []);

  const login = async (email: string, password: string) => {
    dispatch({ type: 'LOGIN_START' });

    try {
      // Call the backend login API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        const userSession: UserSession = {
          ...data.data.user,
          accessToken: data.data.accessToken,
          refreshToken: data.data.refreshToken,
          expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours from now
          createdAt: new Date(),
          updatedAt: new Date(),
        };

        // Store session in localStorage
        localStorage.setItem('userSession', JSON.stringify(userSession));

        dispatch({ type: 'LOGIN_SUCCESS', payload: userSession });
      } else {
        const errorMessage = data.message || 'Login failed';
        dispatch({ type: 'LOGIN_ERROR', payload: errorMessage });
        throw new Error(errorMessage);
      }
    } catch (error: any) {
      const errorMessage = error.message || 'An error occurred during login';
      dispatch({ type: 'LOGIN_ERROR', payload: errorMessage });
      throw error;
    }
  };

  const signup = async (name: string, email: string, password: string) => {
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      // Call the backend signup API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // After successful signup, we should log the user in
        // First, try to login the user with provided credentials
        const loginResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        const loginData = await loginResponse.json();

        if (loginResponse.ok && loginData.success) {
          const userSession: UserSession = {
            ...loginData.data.user,
            accessToken: loginData.data.accessToken,
            refreshToken: loginData.data.refreshToken,
            expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours from now
            createdAt: new Date(loginData.data.user.createdAt),
            updatedAt: new Date(loginData.data.user.updatedAt),
          };

          // Store session in localStorage
          localStorage.setItem('userSession', JSON.stringify(userSession));

          dispatch({ type: 'LOGIN_SUCCESS', payload: userSession });
        } else {
          const errorMessage = loginData.message || 'Login failed after signup';
          dispatch({ type: 'LOGIN_ERROR', payload: errorMessage });
          throw new Error(errorMessage);
        }
      } else {
        const errorMessage = data.message || 'Signup failed';
        dispatch({ type: 'SIGNUP_ERROR', payload: errorMessage });
        throw new Error(errorMessage);
      }
    } catch (error: any) {
      const errorMessage = error.message || 'An error occurred during signup';
      dispatch({ type: 'SIGNUP_ERROR', payload: errorMessage });
      throw error;
    }
  };

  const logout = () => {
    // Remove session from localStorage
    localStorage.removeItem('userSession');
    localStorage.removeItem('accessToken');

    dispatch({ type: 'LOGOUT' });
  };

  const updateUser = (userData: Partial<UserSession>) => {
    dispatch({ type: 'UPDATE_USER', payload: userData });

    // Update session in localStorage if user exists
    if (state.user) {
      const updatedSession = { ...state.user, ...userData };
      localStorage.setItem('userSession', JSON.stringify(updatedSession));
    }
  };

  const value = {
    state,
    login,
    signup,
    logout,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};