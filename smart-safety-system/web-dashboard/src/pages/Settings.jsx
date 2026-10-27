import { useEffect, useState } from "react";
import { request } from "../api";

export default function Settings() {
  const [s, setS] = useState(null);
  const [form, setForm] = useState({});
  useEffect(() => { request("/api/settings").then(d => { setS(d); setForm(d); }); }, []);
  async function save(e) {
    e.preventDefault();
    await request("/api/settings", { method: "PUT", body: JSON.stringify(form) });
    alert("Saved");
  }
  if (!s) return <p>Loading...</p>;
  const fields = ["heartbeat_timeout_seconds", "event_window_seconds", "failed_login_threshold", "alert_threshold_score", "retention_days"];
  return (
    <div>
      <h1>Settings</h1>
      <form onSubmit={save}>
        {fields.map(f => (
          <div key={f} style={{ marginBottom: 8 }}>
            <label>{f}: </label>
            <input type="number" value={form[f] ?? ""} onChange={e => setForm({ ...form, [f]: Number(e.target.value) })} />
          </div>
        ))}
        <button type="submit">Save</button>
      </form>
    </div>
  );
}
