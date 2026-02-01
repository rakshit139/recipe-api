import { useState } from "react";
import api from "../api/client";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", res.data.access_token);
      window.location.href = "/";
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="h-screen flex flex-col items-center justify-center">
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <form
        onSubmit={handleSubmit}
        className="p-6 bg-white shadow rounded w-80"
      >
        <h2 className="text-xl font-bold mb-4">Login</h2>

        <input
          className="border p-2 w-full mb-3"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          className="border p-2 w-full mb-3"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="bg-blue-500 text-white w-full p-2">Login</button>
      </form>
    </div>
  );
}
