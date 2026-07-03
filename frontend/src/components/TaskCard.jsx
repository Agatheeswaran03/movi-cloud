export default function TaskCard({ task, onEdit, onDelete }) {
  const formatDate = (dateStr) => {
    if (!dateStr) return null;
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const isOverdue = () => {
    if (!task.due_date || task.status === 'completed') return false;
    return new Date(task.due_date) < new Date();
  };

  const statusLabel = {
    pending: 'Pending',
    in_progress: 'In Progress',
    completed: 'Completed',
  };

  return (
    <div className={`task-card card status-${task.status}`}>
      <div className="task-card-header">
        <h3 className="task-title">{task.title}</h3>
        <div className="task-actions">
          <button
            className="task-action-btn"
            onClick={() => onEdit(task)}
            title="Edit task"
            aria-label="Edit task"
          >
            ✏️
          </button>
          <button
            className="task-action-btn delete"
            onClick={() => onDelete(task)}
            title="Delete task"
            aria-label="Delete task"
          >
            🗑️
          </button>
        </div>
      </div>

      {task.description && (
        <p className="task-description">{task.description}</p>
      )}

      <div className="task-footer">
        <span className={`badge badge-${task.status}`}>
          {task.status === 'completed' && '✓ '}
          {task.status === 'in_progress' && '◐ '}
          {task.status === 'pending' && '○ '}
          {statusLabel[task.status]}
        </span>

        {task.due_date && (
          <span className={`task-due ${isOverdue() ? 'overdue' : ''}`}>
            📅 {formatDate(task.due_date)}
            {isOverdue() && ' (Overdue)'}
          </span>
        )}
      </div>
    </div>
  );
}
