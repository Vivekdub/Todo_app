import React, { useEffect, useState } from "react";
import { listTasks, createTask, deleteTask, completeTask } from "../api.js";
import { useNavigate } from "react-router-dom";
import TaskForm from "../components/TaskForm.jsx";
import TaskList from "../components/TaskList.jsx";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const navigate = useNavigate();

  async function fetchTasks() {
    try {
      const res = await listTasks();
      setTasks(res.data);
    } catch {
      navigate("/login");
    }
  }

  useEffect(() => { fetchTasks(); }, []);

  const handleAddTask = async (data) => {
    await createTask(data);
    setShowForm(false);
    fetchTasks();
  };

  const handleComplete = async (id) => {
    await completeTask(id);
    fetchTasks();
  };

  const handleDelete = async (id) => {
    await deleteTask(id);
    fetchTasks();
  };

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="container">
      <h2>My Tasks</h2>
      <button onClick={() => setShowForm(!showForm)}>
        {showForm ? "Close" : "Add Task"}
      </button>
      <button onClick={logout} style={{ marginLeft: "1em" }}>Logout</button>

      {showForm && <TaskForm onSubmit={handleAddTask} />}
      <TaskList tasks={tasks} onComplete={handleComplete} onDelete={handleDelete} />
    </div>
  );
}
