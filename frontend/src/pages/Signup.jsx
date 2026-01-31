import { useState } from "react";
import { signup } from "../api/auth.api";
import { Link, useNavigate } from "react-router-dom";

export default function Signup() {
  const [form, setForm] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    await signup(form);
    navigate("/login");
  };

  return (
    <div className="auth-container">
      <h2>Create Account</h2>
      <form onSubmit={submit}>
        <input placeholder="Email" onChange={e => setForm({...form,email:e.target.value})} />
        <input type="password" placeholder="Password" onChange={e => setForm({...form,password:e.target.value})} />
        <button>Create Account</button>
      </form>
      <p>Already have an account? <Link to="/login">Login</Link></p>
    </div>
  );
}
