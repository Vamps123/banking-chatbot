import axios from "axios";

const baseUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getHealth() {
  const response = await axios.get(`${baseUrl}/health`);
  return response.data;
}

export async function sendMessage(payload) {
  const response = await axios.post(`${baseUrl}/chat`, payload);
  return response.data;
}

export async function uploadDocument(file) {
  const form = new FormData();
  form.append("file", file);
  const response = await axios.post(`${baseUrl}/upload`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}
