import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";
import { useState } from "react";
import { request, getToken, setToken, clearToken } from "./api";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Devices from "./pages/Devices";
import Alerts from "./pages/Alerts";
import Events from "./pages/Events";
import Settings from "./pages/Settings";
import DSAPage from "./pages/DSAPage";

function Nav() {
  return (
    <nav style={{ display: "flex", gap: 12, padding: 12, background: "#0f172a", color: "white" }}>
      <Link to="/dashboard" style={{ color: "white" }}>Dashboard</Link>
      <Link to="/devices" style={{ color: "white" }}>Devices</Link>
      <Link to="/alerts" style={{ color: "white" }}>Alerts</Link>
      <Link to="/events" style={{ color: "white" }}>Events</Link>
      <Link to="/dsa" style={{ color: "white" }}>DSA Demo</Link>
      <Link to="/settings" style={{ color: "white" }}>Settings</Link>
      <button onClick={() => { clearToken(); window.location.href = "/login"; }} style={{ marginLeft: "auto" }}>Logout</button>
    </nav>
  );
}

function Private({ children }) {
  return getToken() ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/*" element={
          <Private>
            <Nav />
            <div style={{ padding: 16 }}>
              <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/devices" element={<Devices />} />
                <Route path="/alerts" element={<Alerts />} />
                <Route path="/events" element={<Events />} />
                <Route path="/dsa" element={<DSAPage />} />
                <Route path="/settings" element={<Settings />} />
                <Route path="*" element={<Navigate to="/dashboard" />} />
              </Routes>
            </div>
          </Private>
        } />
      </Routes>
    </BrowserRouter>
  );
}
