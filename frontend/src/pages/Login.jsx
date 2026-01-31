import { useState } from "react";
import { login } from "../api/auth.api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    const res = await login(form);
    localStorage.setItem("token", res.data.access_token);
    navigate("/dashboard");
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      <form onSubmit={submit}>
        <input placeholder="Email" onChange={e => setForm({...form,email:e.target.value})} />
        <input type="password" placeholder="Password" onChange={e => setForm({...form,password:e.target.value})} />
        <button>Login</button>
      </form>
    </div>
  );
}
