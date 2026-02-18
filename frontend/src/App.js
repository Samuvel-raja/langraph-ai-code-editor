import React, { useState } from "react";
import axios from "axios";
import Editor from "@monaco-editor/react";

const BACKEND = "http://127.0.0.1:8000";

function App() {
  const [task, setTask] = useState("");
  const [plan, setPlan] = useState([]);
  const [files, setFiles] = useState({});
  const [selectedFile, setSelectedFile] = useState(null);
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const runTask = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await axios.post(
        `${BACKEND}/run`,
        null, 
        { params: { task: task } }
      );

      const data = res.data;

      // Ensure we have valid data structures
      const safePlan = Array.isArray(data.plan) ? data.plan : [];
      const safeFiles = data.files && typeof data.files === "object" ? data.files : {};

      setPlan(safePlan);
      setFiles(safeFiles);
      setOutput(data.output || "");
      
      const keys = Object.keys(safeFiles);
      if (keys.length > 0) {
        setSelectedFile(keys[0]);
      } else {
        setSelectedFile(null);
      }
    } catch (e) {
      setError(`Error: ${e.response?.data?.detail || e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const updateFile = (value) => {
    if (!selectedFile) return;
    setFiles((prev) => ({
      ...prev,
      [selectedFile]: value || "",
    }));
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif" }}>
      {/* Sidebar */}
      <div style={{ width: "300px", padding: "20px", borderRight: "1px solid #ccc", overflowY: "auto", backgroundColor: "#f9f9f9" }}>
        <h3>Task</h3>
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          style={{ width: "100%", height: "80px", marginBottom: "10px", padding: "8px" }}
          placeholder="Enter task description..."
        />
        <button 
          onClick={runTask} 
          disabled={loading}
          style={{ width: "100%", padding: "10px", cursor: "pointer", backgroundColor: "#007bff", color: "white", border: "none", borderRadius: "4px" }}
        >
          {loading ? "Running..." : "Run Task"}
        </button>

        <h3>Plan</h3>
        <div style={{ fontSize: "14px", lineHeight: "1.6" }}>
          {plan.map((step, i) => (
            <div key={i} style={{ marginBottom: "5px" }}>
              <strong>{i + 1}.</strong> {step}
            </div>
          ))}
        </div>

        <h3>Files</h3>
        {Object.keys(files).map((file) => (
          <div
            key={file}
            onClick={() => setSelectedFile(file)}
            style={{
              padding: "8px",
              cursor: "pointer",
              borderRadius: "4px",
              marginBottom: "4px",
              background: selectedFile === file ? "#007bff" : "#eee",
              color: selectedFile === file ? "white" : "black",
              fontSize: "13px"
            }}
          >
            {file}
          </div>
        ))}
      </div>

      {/* Main Content Area */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", padding: "20px" }}>
        <div style={{ flex: 1, minHeight: "400px", border: "1px solid #ccc" }}>
          {selectedFile ? (
            <Editor
              height="100%"
              language="python"
              theme="vs-dark"
              value={files[selectedFile]}
              onChange={updateFile}
              options={{ fontSize: 14, minimap: { enabled: false } }}
            />
          ) : (
            <div style={{ padding: "20px", color: "#666" }}>Select a file to edit or run a task to generate files.</div>
          )}
        </div>

        <div style={{ height: "250px", marginTop: "20px", overflowY: "auto" }}>
          <h3>Output</h3>
          <pre style={{ background: "#222", color: "#0f0", padding: "15px", borderRadius: "5px", minHeight: "50px" }}>
            {output || "No output yet."}
          </pre>

          {error && (
            <div style={{ marginTop: "10px", padding: "10px", background: "#fee", color: "red", border: "1px solid red", borderRadius: "4px" }}>
              {error}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;