import { useState } from "react";
import { request, setToken } from "../api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPass] = useState("");
  const [name, setName] = useState("");
  const [mode, setMode] = useState("login");
  const [err, setErr] = useState("");

  async function submit(e) {
    e.preventDefault();
    try {
      if (mode === "register") {
        await request("/api/auth/register", { method: "POST", body: JSON.stringify({ email, full_name: name, password }) });
      }
      const r = await request("/api/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
      setToken(r.access_token);
      window.location.href = "/dashboard";
    } catch (e) { setErr(e.message); }
  }

  return (
    <div style={{ maxWidth: 360, margin: "80px auto", padding: 20, border: "1px solid #ddd", borderRadius: 8 }}>
      <h2>{mode === "login" ? "Login" : "Register"}</h2>
      <form onSubmit={submit}>
        {mode === "register" && <input placeholder="Full name" value={name} onChange={e => setName(e.target.value)} style={{ width: "100%", marginBottom: 8 }} />}
        <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} style={{ width: "100%", marginBottom: 8 }} />
        <input placeholder="Password" type="password" value={password} onChange={e => setPass(e.target.value)} style={{ width: "100%", marginBottom: 8 }} />
        <button type="submit" style={{ width: "100%" }}>{mode === "login" ? "Login" : "Register"}</button>
      </form>
      <p style={{ color: "red" }}>{err}</p>
      <button onClick={() => setMode(mode === "login" ? "register" : "login")} style={{ background: "none", border: "none", color: "blue", cursor: "pointer" }}>
        {mode === "login" ? "Need an account? Register" : "Have account? Login"}
      </button>
    </div>
  );
}
