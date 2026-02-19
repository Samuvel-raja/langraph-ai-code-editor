import React, { useEffect, useState } from "react";
import { fetchFiles } from "./apiurll";

export default function FileTree({ onSelect }) {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const data = await fetchFiles();
        if (cancelled) return;

        let normalized = [];

        if (Array.isArray(data)) {
          // Array of strings or objects
          normalized = data.map((item) =>
            typeof item === "string"
              ? { name: item, path: item }
              : { name: item.name || item.path, path: item.path || item.name }
          );
        } else if (data && typeof data === "object") {
          // Object mapping filename -> content
          normalized = Object.keys(data).map((key) => ({
            name: key,
            path: key,
          }));
        }

        setFiles(normalized);
      } catch (e) {
        console.error("Failed to fetch files from API", e);
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div style={{ color: "#fff", fontSize: "13px", padding: "8px 0" }}>
      {files.map((file) => (
        <div
          key={file.path}
          style={{
            padding: "4px 12px",
            cursor: "pointer",
            whiteSpace: "nowrap",
            textOverflow: "ellipsis",
            overflow: "hidden",
          }}
          onClick={() => onSelect && onSelect(file.path)}
        >
          {file.name}
        </div>
      ))}
    </div>
  );
}
