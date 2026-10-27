const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export function getToken() { return localStorage.getItem("token"); }
export function setToken(t) { localStorage.setItem("token", t); }
export function clearToken() { localStorage.removeItem("token"); }

export async function request(path, opts = {}) {
  const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
  const t = getToken();
  if (t) headers.Authorization = `Bearer ${t}`;
  const res = await fetch(API + path, { ...opts, headers });
  if (res.status === 401) { clearToken(); throw new Error("Unauthorized"); }
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt || res.statusText);
  }
  if (res.status === 204) return null;
  return res.json();
}
