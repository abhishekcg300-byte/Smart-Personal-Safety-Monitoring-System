import { useEffect, useState } from "react";
import { request } from "../api";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [filters] = useState({});
  useEffect(() => { request("/api/alerts").then(setAlerts).catch(console.error); }, []);
  return (
    <div>
      <h1>Alerts</h1>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead><tr><th>ID</th><th>Type</th><th>Severity</th><th>Risk</th><th>Status</th><th>Time</th><th>Explanation</th></tr></thead>
        <tbody>
          {alerts.map(a => (
            <tr key={a.id} style={{ borderBottom: "1px solid #eee" }}>
              <td>{a.id}</td><td>{a.alert_type}</td><td>{a.severity}</td><td>{a.risk_score}</td><td>{a.status}</td><td>{a.created_at}</td><td style={{ maxWidth: 300 }}>{a.explanation}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
