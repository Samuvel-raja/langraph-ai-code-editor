import React, { useEffect, useRef } from "react";
import { Terminal } from "xterm";
import "xterm/css/xterm.css";

export default function TerminalComponent() {
  const ref = useRef(null);
  const termRef = useRef(null);

  useEffect(() => {
    // Avoid creating multiple terminals in React StrictMode/dev
    if (!ref.current || termRef.current) return;

    const term = new Terminal({
      rows: 10,
      theme: {
        background: "#1e1e1e",
      },
    });
    termRef.current = term;

    term.open(ref.current);

    term.write("Windsurf Terminal Ready\r\n");

    term.prompt = () => {
      term.write("\r\n$ ");
    };

    term.prompt();

    term.onData((data) => {
      term.write(data);
    });

    return () => {
      if (termRef.current) {
        termRef.current.dispose();
        termRef.current = null;
      }
      if (ref.current) {
        ref.current.innerHTML = "";
      }
    };
  }, []);

  return (
    <div
      ref={ref}
      style={{
        height: "200px",
        background: "#1e1e1e",
        borderTop: "1px solid #333",
      }}
    />
  );
}
