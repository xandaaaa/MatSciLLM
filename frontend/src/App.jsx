import { useState } from "react";

function App() {
  const [activeTab, setActiveTab] = useState("ask");
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

  const handleSummarize = async () => {
    setResponse("");
    setLoading(true);
    const res = await fetch("http://localhost:8000/summarizer", {
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

      {/* Tab Buttons */}
      <div style={{ marginBottom: "1rem" }}>
        <button
          onClick={() => setActiveTab("ask")}
          style={{ marginRight: "1rem", fontWeight: activeTab === "ask" ? "bold" : "normal" }}
        >
          Ask LLM
        </button>
        <button
          onClick={() => setActiveTab("summarizer")}
          style={{ marginRight: "1rem", fontWeight: activeTab === "summarizer" ? "bold" : "normal" }}
        >
          Summarize LLM
        </button>
        <button
          onClick={() => setActiveTab("third")}
          style={{ fontWeight: activeTab === "third" ? "bold" : "normal" }}
        >
          Placeholder
        </button>
      </div>

      {/* Tab Contents */}
      {activeTab === "ask" && (
        <>
          <p style={{ color: "#555" }}>
            Template: Tell me something about the [property] of [material].
          </p>
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
        </>
      )}

      {activeTab === "summarizer" && (
        <>
          <p style={{ color: "#555" }}>
            Enter a topic to get a summary from the vector store.
          </p>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type your topic..."
            rows={3}
            style={{ width: "100%", fontSize: "1rem" }}
          />
          <br />
          <button onClick={handleSummarize} disabled={loading} style={{ marginTop: "1rem" }}>
            {loading ? "Summarizing..." : "Summarize"}
          </button>
          <pre style={{ whiteSpace: "pre-wrap", marginTop: "1rem" }}>{response}</pre>
        </>
      )}

      {activeTab === "third" && (
        <div>
          <p>Hi.</p>
        </div>
      )}
    </div>
  );
}

export default App;