import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

export function setToken(token) {
  if (token) api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  else delete api.defaults.headers.common["Authorization"];
}

// Auth
export const signup = (email, password) =>
  api.post("/auth/signup", { email, password });
export const login = (email, password) =>
  api.post("/auth/login", { email, password });

// Tasks
export const listTasks = () => api.get("/tasks");
export const createTask = (data) => api.post("/tasks", data);
export const updateTask = (id, data) => api.put(`/tasks/${id}`, data);
export const completeTask = (id) => api.post(`/tasks/${id}/complete`);
export const deleteTask = (id) => api.delete(`/tasks/${id}`);
