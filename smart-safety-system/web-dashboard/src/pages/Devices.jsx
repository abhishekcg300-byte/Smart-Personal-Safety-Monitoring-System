import { useEffect, useState } from "react";
import { request } from "../api";

export default function Devices() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [uid, setUid] = useState("");
  const [name, setName] = useState("");
  const [registering, setRegistering] = useState(false);

  async function load() {
    try {
      const data = await request("/api/devices");
      setDevices(Array.isArray(data) ? data : []);
    } catch (e) {
      setError(e.message || "Failed to load devices");
      setDevices([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // Do not return the promise from load(); useEffect must return
    // undefined or a cleanup function.
  }, []);

  async function register(e) {
    e.preventDefault();
    setRegistering(true);
    setError("");
    try {
      await request("/api/devices/register", { method: "POST", body: JSON.stringify({ device_uid: uid, name }) });
      setUid(""); setName("");
      await load();
    } catch (err) {
      setError(err.message || "Failed to register device");
    } finally {
      setRegistering(false);
    }
  }

  return (
    <div>
      <h1>Devices</h1>
      <form onSubmit={register} style={{ marginBottom: 16 }}>
        <input placeholder="Device UID" value={uid} onChange={e => setUid(e.target.value)} />
        <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
        <button type="submit" disabled={registering}>{registering ? "Registering..." : "Register device"}</button>
      </form>

      {loading && <p>Loading devices...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && devices.length === 0 && (
        <p style={{ color: "#64748b" }}>No devices registered yet. Register your first device above.</p>
      )}

      {!loading && devices.length > 0 && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead><tr><th>ID</th><th>UID</th><th>Name</th><th>Status</th><th>Last heartbeat</th></tr></thead>
          <tbody>
            {devices.map(d => (
              <tr key={d.id} style={{ borderBottom: "1px solid #eee" }}>
                <td>{d.id}</td><td>{d.device_uid}</td><td>{d.name}</td><td>{d.status}</td><td>{d.last_heartbeat || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <p style={{ marginTop: 12, fontSize: 13, color: "#64748b" }}>
        Use the mobile app or POST /api/devices/{"{id}"}/heartbeat to update status.
      </p>
    </div>
  );
}
