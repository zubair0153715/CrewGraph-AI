'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { agentAPI, taskAPI } from '@/lib/api';
import { LogOut, Plus, Play, Trash2, Users, FileText, Brain } from 'lucide-react';

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout, isAuthenticated } = useAuthStore();
  const [agents, setAgents] = useState<any[]>([]);
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateAgent, setShowCreateAgent] = useState(false);
  const [newAgent, setNewAgent] = useState({
    name: '',
    role: '',
    description: '',
    autonomy_level: 'medium',
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    loadData();
  }, [isAuthenticated, router]);

  const loadData = async () => {
    try {
      const [agentsRes, tasksRes] = await Promise.all([
        agentAPI.list(),
        taskAPI.list(),
      ]);
      setAgents(agentsRes.data);
      setTasks(tasksRes.data);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await agentAPI.create(newAgent);
      setShowCreateAgent(false);
      setNewAgent({ name: '', role: '', description: '', autonomy_level: 'medium' });
      loadData();
    } catch (error) {
      console.error('Failed to create agent:', error);
    }
  };

  const handleDeleteAgent = async (id: string) => {
    if (!confirm('Are you sure you want to delete this agent?')) return;
    try {
      await agentAPI.delete(id);
      loadData();
    } catch (error) {
      console.error('Failed to delete agent:', error);
    }
  };

  const handleExecuteTask = async (agentId: string) => {
    const description = prompt('Enter task description:');
    if (!description) return;

    try {
      const task = await taskAPI.create({
        agent_id: agentId,
        title: `Task for ${agents.find(a => a.id === agentId)?.name}`,
        description,
      });
      
      alert('Task created! Starting execution...');
      
      // Execute the task
      const result = await taskAPI.execute(task.data.id);
      alert(`Task completed!\n\nResult:\n${result.data.result}`);
      
      loadData();
    } catch (error: any) {
      alert(`Task failed: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  if (!isAuthenticated || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Navigation */}
      <nav className="bg-white dark:bg-gray-800 shadow-sm border-b dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Brain className="h-8 w-8 text-primary-600" />
              <h1 className="ml-2 text-xl font-bold text-gray-900 dark:text-white">AgentOS</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600 dark:text-gray-300">
                {user?.full_name || user?.email}
              </span>
              <button
                onClick={handleLogout}
                className="flex items-center px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center">
              <Users className="h-10 w-10 text-primary-600" />
              <div className="ml-4">
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Agents</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{agents.length}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center">
              <FileText className="h-10 w-10 text-green-600" />
              <div className="ml-4">
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Tasks</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{tasks.length}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center">
              <Brain className="h-10 w-10 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm text-gray-600 dark:text-gray-400">Completed Tasks</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {tasks.filter(t => t.status === 'completed').length}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Agents Section */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">My Agents</h2>
            <button
              onClick={() => setShowCreateAgent(!showCreateAgent)}
              className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
            >
              <Plus className="h-4 w-4 mr-2" />
              Create Agent
            </button>
          </div>

          {showCreateAgent && (
            <form onSubmit={handleCreateAgent} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
              <h3 className="text-lg font-semibold mb-4">Create New Agent</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Name</label>
                  <input
                    type="text"
                    value={newAgent.name}
                    onChange={(e) => setNewAgent({...newAgent, name: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md dark:bg-gray-700 dark:border-gray-600"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Role</label>
                  <input
                    type="text"
                    value={newAgent.role}
                    onChange={(e) => setNewAgent({...newAgent, role: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md dark:bg-gray-700 dark:border-gray-600"
                    placeholder="e.g., Research Analyst"
                    required
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium mb-1">Description</label>
                  <textarea
                    value={newAgent.description}
                    onChange={(e) => setNewAgent({...newAgent, description: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md dark:bg-gray-700 dark:border-gray-600"
                    rows={3}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Autonomy Level</label>
                  <select
                    value={newAgent.autonomy_level}
                    onChange={(e) => setNewAgent({...newAgent, autonomy_level: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md dark:bg-gray-700 dark:border-gray-600"
                  >
                    <option value="low">Low (Ask for confirmation)</option>
                    <option value="medium">Medium (Routine decisions)</option>
                    <option value="high">High (Full autonomy)</option>
                  </select>
                </div>
              </div>
              <div className="mt-4 flex space-x-2">
                <button type="submit" className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700">
                  Create Agent
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateAgent(false)}
                  className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <div key={agent.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold">{agent.name}</h3>
                    <p className="text-sm text-primary-600">{agent.role}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    agent.autonomy_level === 'high' ? 'bg-green-100 text-green-800' :
                    agent.autonomy_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {agent.autonomy_level}
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">{agent.description}</p>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleExecuteTask(agent.id)}
                    className="flex-1 flex items-center justify-center px-3 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 text-sm"
                  >
                    <Play className="h-4 w-4 mr-1" />
                    Run Task
                  </button>
                  <button
                    onClick={() => handleDeleteAgent(agent.id)}
                    className="px-3 py-2 bg-red-100 dark:bg-red-900/30 text-red-600 rounded-md hover:bg-red-200 dark:hover:bg-red-900/50"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
            
            {agents.length === 0 && (
              <div className="col-span-full text-center py-12 text-gray-500 dark:text-gray-400">
                No agents yet. Create your first AI agent!
              </div>
            )}
          </div>
        </div>

        {/* Recent Tasks */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Recent Tasks</h2>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Task</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Created</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {tasks.slice(0, 5).map((task) => (
                  <tr key={task.id}>
                    <td className="px-6 py-4">
                      <div>
                        <p className="font-medium">{task.title}</p>
                        <p className="text-sm text-gray-500 dark:text-gray-400 truncate max-w-md">{task.description}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        task.status === 'completed' ? 'bg-green-100 text-green-800' :
                        task.status === 'running' ? 'bg-blue-100 text-blue-800' :
                        task.status === 'failed' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {task.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {new Date(task.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
                {tasks.length === 0 && (
                  <tr>
                    <td colSpan={3} className="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                      No tasks yet
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
