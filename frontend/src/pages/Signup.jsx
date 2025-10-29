import React, { useState } from "react";
import { signup } from "../api.js";
import { Link, useNavigate } from "react-router-dom";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signup(email, password);
      setMsg("Account created! Redirecting...");
      setTimeout(() => navigate("/login"), 1000);
    } catch {
      setMsg("Email already exists or invalid input");
    }
  };

  return (
    <div className="container">
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="Email" value={email}
          onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" value={password}
          onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Create Account</button>
      </form>
      <p>{msg}</p>
      <p>Already have an account? <Link to="/login">Login</Link></p>
    </div>
  );
}
