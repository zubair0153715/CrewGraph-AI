'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { authAPI } from '@/lib/api';

export default function Home() {
  const router = useRouter();
  const { isAuthenticated, user } = useAuthStore();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
      <nav className="border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">AgentOS</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-600 dark:text-gray-300">
                {user?.full_name || user?.email}
              </span>
              <button
                onClick={() => router.push('/dashboard')}
                className="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700"
              >
                Dashboard
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Welcome to AgentOS
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            Your AI Agent Operating System
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
              <div className="text-primary-600 text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold mb-2">Create Agents</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Build your AI team with specialized agents for different tasks
              </p>
            </div>
            
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
              <div className="text-primary-600 text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold mb-2">Automate Tasks</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Assign tasks to your agents and let them work automatically
              </p>
            </div>
            
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
              <div className="text-primary-600 text-4xl mb-4">🧠</div>
              <h3 className="text-xl font-semibold mb-2">Learn & Improve</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Agents learn from past tasks and improve over time
              </p>
            </div>
          </div>

          <button
            onClick={() => router.push('/dashboard')}
            className="mt-12 px-8 py-3 text-lg font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700 transition-colors"
          >
            Get Started →
          </button>
        </div>
      </main>
    </div>
  );
}
