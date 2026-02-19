export const GET_FILES_URL = "http://localhost:8000/files";
export const GET_FILE_CONTENT_URL = "http://localhost:8000/file";
export const GENERATE_CODE_URL = "http://localhost:8000/run";

export async function fetchFiles() {
  const res = await fetch(GET_FILES_URL);
  if (!res.ok) {
    throw new Error(`Failed to fetch files: ${res.status}`);
  }
  return res.json();
}

export async function fetchFileContent(path) {
  const res = await fetch(`${GET_FILE_CONTENT_URL}?name=${encodeURIComponent(path)}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch file content: ${res.status}`);
  }
  return res.json();
}

export async function generateCode(payload) {
  const res = await fetch(`${GENERATE_CODE_URL}?task=${encodeURIComponent(payload.prompt)}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: [],
  });

  if (!res.ok) {
    throw new Error(`Failed to generate code: ${res.status}`);
  }

  return res.json();
}