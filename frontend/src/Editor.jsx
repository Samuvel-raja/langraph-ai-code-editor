import React, { useEffect, useState } from "react";
import Editor from "@monaco-editor/react";
import { getFS } from "./filesystem";

export default function CodeEditor({ file }) {
  const [code, setCode] = useState("");

  useEffect(() => {
    if (!file) return;

    const fs = getFS();
    if (!fs) return;

    try {
      const content = fs.readFileSync("/" + file, "utf-8");
      setCode(content);
    } catch (e) {
      console.error("Failed to read file from BrowserFS", e);
      setCode("");
    }
  }, [file]);

  function handleChange(value) {
    setCode(value);

    const fs = getFS();
    if (!fs || !file) return;

    try {
      fs.writeFileSync("/" + file, value);
    } catch (e) {
      console.error("Failed to write file to BrowserFS", e);
    }
  }

  return (
    <Editor
      height="100%"
      theme="vs-dark"
      language="python"
      value={code}
      onChange={handleChange}
    />
  );
}
