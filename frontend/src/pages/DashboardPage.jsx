import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import API from '../api/axios';
import TaskCard from '../components/TaskCard';
import TaskModal from '../components/TaskModal';
import ConfirmDialog from '../components/ConfirmDialog';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  // Modal states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  // Confirm dialog states
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [deletingTask, setDeletingTask] = useState(null);

  // Fetch tasks from API
  const fetchTasks = useCallback(async () => {
    try {
      const response = await API.get('/tasks');
      setTasks(response.data.tasks);
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Create or update task
  const handleSubmitTask = async (taskData, taskId) => {
    if (taskId) {
      // Update
      await API.put(`/tasks/${taskId}`, taskData);
    } else {
      // Create
      await API.post('/tasks', taskData);
    }
    await fetchTasks();
  };

  // Delete task
  const handleDeleteTask = async () => {
    if (!deletingTask) return;
    try {
      await API.delete(`/tasks/${deletingTask.id}`);
      await fetchTasks();
    } catch (err) {
      console.error('Failed to delete task:', err);
    } finally {
      setIsConfirmOpen(false);
      setDeletingTask(null);
    }
  };

  // Open modals
  const openCreate = () => {
    setEditingTask(null);
    setIsModalOpen(true);
  };

  const openEdit = (task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const openDelete = (task) => {
    setDeletingTask(task);
    setIsConfirmOpen(true);
  };

  // Filtered tasks
  const filteredTasks =
    filter === 'all'
      ? tasks
      : tasks.filter((t) => t.status === filter);

  // Stats
  const stats = {
    total: tasks.length,
    pending: tasks.filter((t) => t.status === 'pending').length,
    in_progress: tasks.filter((t) => t.status === 'in_progress').length,
    completed: tasks.filter((t) => t.status === 'completed').length,
  };

  const getInitials = (name) => {
    if (!name) return '?';
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <h1 className="header-brand">
          Task<span>Flow</span>
        </h1>
        <div className="header-right">
          <div className="header-user">
            <div className="header-avatar">{getInitials(user?.name)}</div>
            <span>{user?.name}</span>
          </div>
          <button className="btn btn-ghost btn-sm" onClick={logout}>
            Sign Out
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-content">
        {/* Stats */}
        <div className="stats-row">
          <div className="stat-card card animate-slideUp stagger-1">
            <div className="stat-icon total">📋</div>
            <div className="stat-info">
              <h3>{stats.total}</h3>
              <p>Total Tasks</p>
            </div>
          </div>
          <div className="stat-card card animate-slideUp stagger-2">
            <div className="stat-icon pending">⏳</div>
            <div className="stat-info">
              <h3>{stats.pending}</h3>
              <p>Pending</p>
            </div>
          </div>
          <div className="stat-card card animate-slideUp stagger-3">
            <div className="stat-icon progress">🔄</div>
            <div className="stat-info">
              <h3>{stats.in_progress}</h3>
              <p>In Progress</p>
            </div>
          </div>
          <div className="stat-card card animate-slideUp stagger-4">
            <div className="stat-icon completed">✅</div>
            <div className="stat-info">
              <h3>{stats.completed}</h3>
              <p>Completed</p>
            </div>
          </div>
        </div>

        {/* Toolbar */}
        <div className="toolbar">
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <h2 className="toolbar-title">My Tasks</h2>
            <button className="btn btn-primary btn-sm" onClick={openCreate}>
              + Add Task
            </button>
          </div>

          <div className="filter-tabs">
            {[
              { key: 'all', label: 'All' },
              { key: 'pending', label: 'Pending' },
              { key: 'in_progress', label: 'In Progress' },
              { key: 'completed', label: 'Completed' },
            ].map((f) => (
              <button
                key={f.key}
                className={`filter-tab ${filter === f.key ? 'active' : ''}`}
                onClick={() => setFilter(f.key)}
              >
                {f.label}
                {f.key !== 'all' && (
                  <span style={{ marginLeft: 4, opacity: 0.6 }}>
                    {stats[f.key]}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Task Grid */}
        {isLoading ? (
          <div style={{ textAlign: 'center', padding: 80 }}>
            <div
              className="spinner spinner-gold"
              style={{ width: 40, height: 40, margin: '0 auto' }}
            />
          </div>
        ) : filteredTasks.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">
              {filter === 'all' ? '📝' : '🔍'}
            </div>
            <h3>
              {filter === 'all'
                ? 'No tasks yet'
                : `No ${filter.replace('_', ' ')} tasks`}
            </h3>
            <p>
              {filter === 'all'
                ? 'Create your first task to get started!'
                : 'Try a different filter or create a new task.'}
            </p>
            {filter === 'all' && (
              <button className="btn btn-primary" onClick={openCreate}>
                + Create Your First Task
              </button>
            )}
          </div>
        ) : (
          <div className="task-grid">
            {filteredTasks.map((task, index) => (
              <div
                key={task.id}
                className={`animate-slideUp stagger-${Math.min(index + 1, 6)}`}
              >
                <TaskCard
                  task={task}
                  onEdit={openEdit}
                  onDelete={openDelete}
                />
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Task Modal */}
      <TaskModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingTask(null);
        }}
        onSubmit={handleSubmitTask}
        task={editingTask}
      />

      {/* Confirm Dialog */}
      <ConfirmDialog
        isOpen={isConfirmOpen}
        onClose={() => {
          setIsConfirmOpen(false);
          setDeletingTask(null);
        }}
        onConfirm={handleDeleteTask}
        title="Delete Task"
        message={`Are you sure you want to delete "${deletingTask?.title}"? This action cannot be undone.`}
      />
    </div>
  );
}
