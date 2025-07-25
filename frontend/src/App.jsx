import { useState, useEffect } from "react";

function App() {
  const [activeTab, setActiveTab] = useState("ask");
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [pdfList, setPdfList] = useState([]);

  useEffect(() => {
  fetch("http://localhost:8000/getpdfs")
    .then(res => res.json())
    .then(data => {
      setPdfList(data);
    })
    .catch(err => console.error("Failed to fetch PDFs:", err));
  }, []);

  // Upload PDFs
  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(files);
    setPdfList(files.map((file) => file.name));
  };

  const handleUpload = async () => {
    if (!selectedFiles || selectedFiles.length === 0) return;

    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append("pdfs", selectedFiles[i]);
    }

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        alert("Upload successful!");
      } else {
        alert("Upload failed.");
      }
    } catch (error) {
      alert("Error uploading files.");
      console.error(error);
    }
  };

  // Tab 1: For specific questions in all submitted PDFs
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

  // Tab 2: Information for every PDF
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
      <div className="sidebar">
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
          
          {/* PDF display and adding */}
          <div className="upload-section">
            <div className="pdf-list">
              {pdfList.length > 0 ? (
                pdfList.map((filename, index) => (
                  <div key={index} className="pdf-item">{filename}</div>
                ))
              ) : (
                <div className="pdf-placeholder">No PDFs uploaded</div>
              )}
            </div>

            <div className="button-row">
              <button onClick={() => {
                setSelectedFiles(null);
                setPdfList([]);
              }}>
                Clear
              </button>

            <button onClick={handleUpload}>
              Add
            </button>
            </div>
          </div>
        </div>

      <div className="main-content">

        <div className="chatbox">
          {/* Tab 1 */}
          {activeTab === "ask" && (
            <>
              <p className="instructions">
              Template: Tell me something about the [property] of [material].
              </p>
              <pre className="response">{response}</pre>
              <div className="textarea-container">
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Type your question..."
                  rows={3}
                  className="textarea"
                />
                <button onClick={handleAsk} disabled={loading} className="button">
                  {loading ? "Asking..." : "Ask"}
                </button>
              </div>
            </>
          )}

          {/* Tab 2 */}
          {activeTab === "summarizer" && (
            <>
              <p className="instructions">
                Enter a topic to get a summary of your question for every PDF.
              </p>
              <pre className="response">{response}</pre>
              <div className="textarea-container">
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Type your question..."
                  rows={3}
                  className="textarea"
                />
                <button onClick={handleSummarize} disabled={loading} className="button">
                  {loading ? "Asking..." : "Ask"}
                </button>
              </div>
            </>
          )}

          {/* Tab 3 */}
          {activeTab === "third" && (
            <>
              <p className="instructions">
                Enter a topic to get a placeholder response.
              </p>
              <pre className="response">This is a placeholder response.</pre>
              <div className="textarea-container">
                <textarea
                  placeholder="Type your topic..."
                  rows={3}
                  className="textarea"
                />
                <button disabled className="button">
                  Placeholder
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;