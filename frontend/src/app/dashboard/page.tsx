'use client';

import React from 'react';
import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';

const DashboardPage: React.FC = () => {
  const { state } = useAuth();
  const router = useRouter();

  // Redirect to tasks page as the default dashboard view
  React.useEffect(() => {
    router.push('/dashboard/tasks');
  }, [router]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="py-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Welcome to your Dashboard</h1>

            {state.user && (
              <div className="mb-6">
                <p className="text-lg text-gray-600">
                  Hello, <span className="font-semibold">{state.user.name || state.user.email}</span>!
                </p>
                <p className="text-gray-600 mt-2">
                  You are successfully logged in to your account.
                </p>
              </div>
            )}

            <div className="text-center py-8">
              <p className="text-gray-600">Redirecting to your tasks...</p>
              <div className="mt-4 flex justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;