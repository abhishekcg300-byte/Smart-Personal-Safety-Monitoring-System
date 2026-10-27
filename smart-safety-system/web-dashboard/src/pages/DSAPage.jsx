import { useState } from "react";
import { request } from "../api";

function DSAPage() {
  const [id, setId] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    setData(null);
    const trimmed = id.trim();
    if (!/^\d+$/.test(trimmed)) {
      setError("Enter a valid numeric database device ID (see the Devices page, e.g. 2).");
      return;
    }
    setLoading(true);
    try {
      setData(await request(`/api/dashboard/dsa?device_id=${trimmed}`));
    } catch (e) {
      setError(e.message || "Failed to load DSA demo");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>DSA Demonstration</h1>
      <p style={{ color: "#64748b", marginBottom: 12 }}>
        Enter the numeric database ID shown on the Devices page for one of your registered devices.
        This is not the device UID (for example, TEST-PHONE-001); database IDs are small integers like 2.
      </p>
      <div style={{ marginBottom: 12 }}>
        <input
          value={id}
          onChange={e => setId(e.target.value)}
          placeholder="Database device ID, e.g. 2"
          inputMode="numeric"
        />
        <button onClick={load} disabled={loading}>{loading ? "Loading..." : "Load"}</button>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {loading && <p>Loading DSA state...</p>}

      {data && (
        <div style={{ display: "grid", gap: 16 }}>
          <p style={{ color: "#64748b", fontSize: 13 }}>
            Queues are populated when events are uploaded for this device. Empty queues mean no events
            have been processed yet; they still exercise the implementations below.
          </p>
          <section>
            <h3>Event Queue (FIFO)</h3>
            <pre style={{ background: "#f8fafc", padding: 8 }}>{JSON.stringify(data.fifo_queue, null, 2)}</pre>
          </section>
          <section>
            <h3>Recent Events Circular Queue</h3>
            <pre style={{ background: "#f8fafc", padding: 8 }}>{JSON.stringify(data.circular_queue, null, 2)}</pre>
          </section>
          <section>
            <h3>Hash Table Event Counts</h3>
            <pre style={{ background: "#f8fafc", padding: 8 }}>{JSON.stringify(data.type_counts, null, 2)}</pre>
          </section>
          <section>
            <h3>Priority Queue (by risk)</h3>
            <pre style={{ background: "#f8fafc", padding: 8 }}>{JSON.stringify(data.priority_queue, null, 2)}</pre>
          </section>
        </div>
      )}
    </div>
  );
}

export default DSAPage;
