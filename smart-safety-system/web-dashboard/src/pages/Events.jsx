import { useEffect, useState } from "react";
import { request } from "../api";

export default function Events() {
  const [events, setEvents] = useState([]);
  const [q, setQ] = useState("");
  useEffect(() => { request("/api/events").then(setEvents).catch(console.error); }, []);
  const filtered = events.filter(e => (q ? e.event_type.includes(q.toUpperCase()) : true));
  return (
    <div>
      <h1>Event History</h1>
      <input placeholder="Filter by type" value={q} onChange={e => setQ(e.target.value)} style={{ marginBottom: 12 }} />
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead><tr><th>ID</th><th>Type</th><th>Risk</th><th>Sev</th><th>Lat</th><th>Lng</th><th>Time</th></tr></thead>
        <tbody>
          {filtered.map(e => (
            <tr key={e.id} style={{ borderBottom: "1px solid #eee" }}>
              <td>{e.id}</td><td>{e.event_type}</td><td>{e.risk_score}</td><td>{e.severity}</td>
              <td>{e.latitude ?? "-"}</td><td>{e.longitude ?? "-"}</td><td>{e.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
