import { useEffect, useState } from "react";
import { request } from "../api";

export default function Dashboard() {
  const [data, setData] = useState(null);
  useEffect(() => { request("/api/dashboard/summary").then(setData).catch(console.error); }, []);
  if (!data) return <p>Loading...</p>;
  return (
    <div>
      <h1>Safety Dashboard</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(160px,1fr))", gap: 12 }}>
        {[
          ["Total devices", data.total_devices],
          ["Online", data.online_devices],
          ["Missing heartbeats", data.missing_heartbeats],
          ["Pending alerts", data.pending_alerts],
          ["High-risk events", data.high_risk_events],
        ].map(([l, v]) => (
          <div key={l} style={{ background: "#f1f5f9", padding: 16, borderRadius: 8 }}>
            <div style={{ fontSize: 12, color: "#64748b" }}>{l}</div>
            <div style={{ fontSize: 24, fontWeight: "bold" }}>{v}</div>
          </div>
        ))}
      </div>
      <h2 style={{ marginTop: 20 }}>Recent events</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead><tr><th>ID</th><th>Type</th><th>Risk</th><th>Severity</th><th>Time</th></tr></thead>
        <tbody>
          {data.recent_events.map(e => (
            <tr key={e.id} style={{ borderBottom: "1px solid #eee" }}>
              <td>{e.id}</td><td>{e.event_type}</td><td>{e.risk_score}</td><td>{e.severity}</td><td>{e.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
