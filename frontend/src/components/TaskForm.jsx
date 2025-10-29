import React, { useState } from "react";

export default function TaskForm({ onSubmit }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [dueAt, setDueAt] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ title, description, due_at: dueAt });
    setTitle(""); setDescription(""); setDueAt("");
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <input type="text" placeholder="Task title" value={title}
        onChange={(e) => setTitle(e.target.value)} required />
      <input type="datetime-local" value={dueAt}
        onChange={(e) => setDueAt(e.target.value)} />
      <textarea placeholder="Description (optional)"
        value={description} onChange={(e) => setDescription(e.target.value)} />
      <button type="submit">Add Task</button>
    </form>
  );
}
