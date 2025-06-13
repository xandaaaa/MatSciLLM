import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    setResponse("");
    setLoading(true);
    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      setResponse((prev) => prev + chunk);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>MatSciLLM</h1>
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Type your question..."
        rows={3}
        style={{ width: "100%", fontSize: "1rem" }}
      />
      <br />
      <button onClick={handleAsk} disabled={loading} style={{ marginTop: "1rem" }}>
        {loading ? "Asking..." : "Ask"}
      </button>
      <pre style={{ whiteSpace: "pre-wrap", marginTop: "1rem" }}>{response}</pre>
    </div>
  );
}

export default App;