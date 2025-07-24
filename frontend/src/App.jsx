import { useState } from "react";

function App() {
  const [activeTab, setActiveTab] = useState("ask");
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);


  // For specific questions in all submitted PDFs
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

  // Information for every PDF
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
    <div className="app-container">
      <h1>MatSciLLM</h1>

      {/* Tab Buttons */}
      <div className="tab-buttons">
        <button
          onClick={() => setActiveTab("ask")}
          className={activeTab === "ask" ? "active" : "inactive"}
        >
          Specific Question
        </button>
        <button
          onClick={() => setActiveTab("summarizer")}
          className={activeTab === "summarizer" ? "active" : "inactive"}
        >
          Every PDF
        </button>
        <button
          onClick={() => setActiveTab("third")}
          className={activeTab === "third" ? "active" : "inactive"}
        >
          Placeholder
        </button>
      </div>

      {/* Tab Contents */}
      {activeTab === "ask" && (
        <>
          <p className="instructions">
            Template: Tell me something about the [property] of [material].
          </p>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type your question..."
            rows={3}
            className="textarea"
          />
          <br />
          <button onClick={handleAsk} disabled={loading} className="button">
            {loading ? "Asking..." : "Ask"}
          </button>
          <pre className="response">{response}</pre>
        </>
      )}

      {activeTab === "summarizer" && (
        <>
          <p className="instructions">
            Enter a topic to get a summary of your question for every PDF.
          </p>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type your question..."
            rows={3}
            className="textarea"
          />
          <br />
          <button onClick={handleSummarize} disabled={loading} className="button">
            {loading ? "Asking..." : "Ask"}
          </button>
          <pre className="response">{response}</pre>
        </>
      )}

      {activeTab === "third" && (
        <div>
          <p>Placeholder.</p>
        </div>
      )}
    </div>
  );
}

export default App;