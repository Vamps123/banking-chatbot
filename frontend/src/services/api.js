import axios from "axios";

let cachedBaseUrl = null;

async function getBaseUrl() {
  if (cachedBaseUrl) return cachedBaseUrl;

  // Prefer runtime config served from the static site.
  // Vite will serve files in /public at the site root.
  try {
    const res = await fetch("/config.json", { cache: "no-store" });
    if (res.ok) {
      const cfg = await res.json();
      if (cfg?.VITE_API_URL) {
        cachedBaseUrl = cfg.VITE_API_URL;
        return cachedBaseUrl;
      }
    }
  } catch (_) {
    // ignore; fallback below
  }

  // Fallback to build-time env (useful for local dev)
  cachedBaseUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
  return cachedBaseUrl;
}

export async function getHealth() {
  const baseUrl = await getBaseUrl();
  const response = await axios.get(`${baseUrl}/health`);
  return response.data;
}

export async function sendMessage(payload) {
  const baseUrl = await getBaseUrl();
  const { session_id, message } = payload;

  // Use query params to avoid JSON body parsing issues behind certain proxies/CDNs.
  const response = await axios.post(
    `${baseUrl}/chat?session_id=${encodeURIComponent(session_id)}&message=${encodeURIComponent(message)}`,
    payload
  );
  return response.data;
}


export async function sendMessageStream(payload, onChunk) {
  const baseUrl = await getBaseUrl();

  // SSE requires a GET by default, but we implement SSE by POST.
  // We'll use fetch() to read the text/event-stream manually.
  const res = await fetch(`${baseUrl}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(`Stream request failed: ${res.status}`);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // SSE events separated by double newline
    const parts = buffer.split("\n\n");
    buffer = parts.pop() || "";

    for (const part of parts) {
      const lines = part.split("\n").filter(Boolean);
      let event = null;
      let dataLine = null;
      for (const line of lines) {
        if (line.startsWith("event:")) event = line.replace("event:", "").trim();
        if (line.startsWith("data:")) dataLine = line.replace("data:", "").trim();
      }
      if (!dataLine) continue;
      const data = JSON.parse(dataLine);
      onChunk(event, data);
    }
  }
}


export async function uploadDocument(file) {
  const form = new FormData();
  form.append("file", file);
  const response = await axios.post(`${baseUrl}/upload`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}
