import React, { useEffect, useState } from "react";
import FileTree from "./FileTree";
import CodeEditor from "./Editor";
import Terminal from "./Terminal";
import ChatBox from "./ChatBox";
import { initFS, getFS } from "./filesystem";
import { fetchFileContent } from "./apiurll";

export default function App() {
  const [file, setFile] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    initFS().then(() => {
      setReady(true);
    });
  }, []);

  async function handleSelectFile(path) {
    try {
      const data = await fetchFileContent(path);

      const content =
        typeof data === "string"
          ? data
          : data.content || data.code || JSON.stringify(data);

      const fs = getFS();
      if (fs) {
        try {
          fs.writeFileSync("/" + path, content);
        } catch (e) {
          console.error("Failed to sync file into BrowserFS", e);
        }
      }

      setFile(path);
    } catch (e) {
      console.error("Failed to fetch file content", e);
    }
  }

  if (!ready) return <div>Loading IDE...</div>;

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        background: "#1e1e1e",
        color: "#fff",
        fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      }}
    >
      {/* File Tree */}
      <div
        style={{
          width: 220,
          borderRight: "1px solid #333",
          background: "#252526",
          overflowY: "auto",
        }}
      >
        <FileTree onSelect={handleSelectFile} />
      </div>

      {/* Editor + Chat + Terminal */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          minWidth: 0,
        }}
      >
        {/* Editor + Chat side by side */}
        <div
          style={{
            flex: 1,
            minHeight: 0,
            display: "flex",
            borderBottom: "1px solid #333",
          }}
        >
          <div style={{ flex: 1, minWidth: 0 }}>
            <CodeEditor file={file} />
          </div>

          <div
            style={{
              width: 360,
              borderLeft: "1px solid #333",
              background: "#1e1e1e",
            }}
          >
            <ChatBox />
          </div>
        </div>

        {/* Terminal */}
        <Terminal />
      </div>
    </div>
  );
}
