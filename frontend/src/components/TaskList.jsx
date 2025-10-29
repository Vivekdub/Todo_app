import React from "react";

export default function TaskList({ tasks, onComplete, onDelete }) {
  if (!tasks.length) return <p>No tasks yet.</p>;

  return (
    <table className="task-table">
      <thead>
        <tr>
          <th>Title</th>
          <th>Due</th>
          <th>Status</th>
          <th>Reminder Sent</th> {/* New column for reminder status */}
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {tasks.map((t) => (
          <tr key={t.id}>
            <td>{t.title}</td>
            <td>{t.due_at ? new Date(t.due_at).toLocaleString() : "—"}</td>
            <td>
              <span className={t.is_completed ? "status-completed" : "status-pending"}>
                {t.is_completed ? "✅ Completed" : "⏳ Pending"}
              </span>
            </td>
            <td>
              <span className={t.reminder_sent ? "status-mailed" : "status-pending"}>
                {t.reminder_sent ? "📧 Mailed" : "🚫 Not Sent"}
              </span>
            </td>
            <td className="action-buttons">
              {!t.is_completed && <button onClick={() => onComplete(t.id)}>Mark Done</button>}
              <button className="btn-secondary" onClick={() => onDelete(t.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
