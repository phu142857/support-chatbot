const API_BASE_URL = "http://127.0.0.1:8000";

export async function uploadScreenshot(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/chat/screenshot`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      error?.detail || "Failed to process screenshot."
    );
  }

  return response.json();
}