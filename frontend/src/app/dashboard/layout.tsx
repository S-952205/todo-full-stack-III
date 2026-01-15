'use client';

import React from 'react';
import { AuthProvider } from '@/context/auth-context';
import ProtectedRoute from '@/components/auth/protected-route';
import Navbar from '@/components/navbar/navbar';

const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <AuthProvider>
      <ProtectedRoute fallback={<div>Loading dashboard...</div>}>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main className="py-6">
            {children}
          </main>
        </div>
      </ProtectedRoute>
    </AuthProvider>
  );
};

export default DashboardLayout;