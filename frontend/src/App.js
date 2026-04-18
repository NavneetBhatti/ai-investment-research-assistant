import { useState } from "react";

function App() {
  const [formData, setFormData] = useState({
    ticker: "",
    horizon: "medium",
    risk_level: "medium",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const getSentimentStyle = (sentiment) => {
    const normalized = (sentiment || "").toLowerCase();

    if (normalized.includes("positive")) {
      return { color: "green", label: "🟢 Positive" };
    }

    if (normalized.includes("negative")) {
      return { color: "red", label: "🔴 Negative" };
    }

    return { color: "#666", label: sentiment || "N/A" };
  };

  const handleAnalyze = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch analysis");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const sentimentDisplay = getSentimentStyle(result?.news_sentiment);

  return (
    <div
      style={{
        maxWidth: "900px",
        margin: "0 auto",
        padding: "40px 20px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1 style={{ marginBottom: "8px" }}>AI Investment Research Assistant</h1>
      <p style={{ color: "#555", marginTop: 0 }}>
        Analyze a stock using live market data, fundamentals, news, and scoring logic.
      </p>

      <form
        onSubmit={handleAnalyze}
        style={{
          display: "grid",
          gap: "16px",
          marginTop: "24px",
          padding: "20px",
          border: "1px solid #ddd",
          borderRadius: "10px",
          backgroundColor: "#fafafa",
        }}
      >
        <div>
          <label><strong>Ticker</strong></label>
          <br />
          <input
            type="text"
            name="ticker"
            value={formData.ticker}
            onChange={handleChange}
            placeholder="e.g. AAPL"
            style={{
              width: "100%",
              padding: "10px",
              marginTop: "6px",
              borderRadius: "6px",
              border: "1px solid #ccc",
              boxSizing: "border-box",
            }}
            required
          />
        </div>

        <div>
          <label><strong>Investment Horizon</strong></label>
          <br />
          <select
            name="horizon"
            value={formData.horizon}
            onChange={handleChange}
            style={{
              width: "100%",
              padding: "10px",
              marginTop: "6px",
              borderRadius: "6px",
              border: "1px solid #ccc",
              boxSizing: "border-box",
            }}
          >
            <option value="short">Short</option>
            <option value="medium">Medium</option>
            <option value="long">Long</option>
          </select>
        </div>

        <div>
          <label><strong>Risk Level</strong></label>
          <br />
          <select
            name="risk_level"
            value={formData.risk_level}
            onChange={handleChange}
            style={{
              width: "100%",
              padding: "10px",
              marginTop: "6px",
              borderRadius: "6px",
              border: "1px solid #ccc",
              boxSizing: "border-box",
            }}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <button
          type="submit"
          style={{
            padding: "12px 18px",
            cursor: "pointer",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#111",
            color: "#fff",
            fontWeight: "bold",
          }}
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && (
        <div
          style={{
            marginTop: "20px",
            color: "red",
            padding: "12px",
            border: "1px solid #f3b4b4",
            borderRadius: "8px",
            backgroundColor: "#fff5f5",
          }}
        >
          {error}
        </div>
      )}

      {result && (
        <div
          style={{
            marginTop: "32px",
            display: "grid",
            gap: "20px",
          }}
        >
          <div
            style={{
              padding: "24px",
              border: "1px solid #ddd",
              borderRadius: "10px",
              backgroundColor: "#fff",
            }}
          >
            <h2 style={{ marginTop: 0 }}>
              {result.ticker} - {result.company_name}
            </h2>

            <div style={{ marginTop: "18px" }}>
              <h3 style={{ marginBottom: "8px" }}>Summary</h3>
              <p style={{ marginTop: 0 }}>{result.summary}</p>
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
                gap: "12px",
                marginTop: "24px",
              }}
            >
              <div style={{ padding: "14px", border: "1px solid #eee", borderRadius: "8px" }}>
                <strong>Valuation Score</strong>
                <div style={{ marginTop: "8px", fontSize: "24px" }}>
                  {result.valuation_score !== null && result.valuation_score !== undefined
                    ? `${result.valuation_score}/10`
                    : "N/A"}
                </div>
              </div>

              <div style={{ padding: "14px", border: "1px solid #eee", borderRadius: "8px" }}>
                <strong>Trend Score</strong>
                <div style={{ marginTop: "8px", fontSize: "24px" }}>
                  {result.trend_score !== null && result.trend_score !== undefined
                ? `${result.trend_score}/10`
                : "N/A"}
                </div>
              </div>

              <div style={{ padding: "14px", border: "1px solid #eee", borderRadius: "8px" }}>
                <strong>News Score</strong>
                <div style={{ marginTop: "8px", fontSize: "24px" }}>
                  {result.news_score !== null && result.news_score !== undefined
                  ? `${result.news_score}/10`
                  : "N/A"}
                </div>
              </div>

              <div style={{ padding: "14px", border: "1px solid #eee", borderRadius: "8px" }}>
                <strong>Risk Score</strong>
                <div style={{ marginTop: "8px", fontSize: "24px" }}>
                  {result.risk_score !== null && result.risk_score !== undefined
                    ? `${result.risk_score}/10`
                    : "N/A"}
                </div>
              </div>
            </div>

            <div
              style={{
                marginTop: "20px",
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                gap: "12px",
              }}
            >
              <div style={{ padding: "14px", border: "1px solid #eee", borderRadius: "8px" }}>
                <strong>News Sentiment</strong>
                <div
                  style={{
                    marginTop: "8px",
                    fontSize: "20px",
                    fontWeight: "bold",
                    color: sentimentDisplay.color,
                  }}
                >
                  {sentimentDisplay.label}
                </div>
              </div>

              <div style={{ padding: "14px", border: "1px solid #eee", borderRadius: "8px" }}>
                <strong>Recommendation</strong>
                <div style={{ marginTop: "8px", fontSize: "20px", fontWeight: "bold" }}>
                  {result.recommendation}
                </div>
              </div>

              <div style={{ padding: "14px", border: "1px solid #eee", borderRadius: "8px" }}>
                <strong>Confidence</strong>
                <div style={{ marginTop: "8px", fontSize: "20px", fontWeight: "bold" }}>
                  {result.confidence !== null && result.confidence !== undefined
                    ? `${result.confidence}/10`
                    : "N/A"}
                </div>
              </div>
            </div>
          </div>

          <div
            style={{
              padding: "24px",
              border: "1px solid #ddd",
              borderRadius: "10px",
              backgroundColor: "#fff",
            }}
          >
            <h3 style={{ marginTop: 0 }}>Details</h3>
            <p><strong>Current Price:</strong> {result.current_price || "N/A"}</p>
            <p><strong>Daily Change %:</strong> {result.daily_change_percent || "N/A"}</p>
            <p><strong>P/E Ratio:</strong> {result.pe_ratio || "N/A"}</p>
            <p><strong>EPS:</strong> {result.eps || "N/A"}</p>
            <p><strong>Market Cap:</strong> {result.market_cap || "N/A"}</p>
          </div>

          <div style={{
              padding: "24px",
              border: "1px solid #ddd",
              borderRadius: "10px",
              backgroundColor: "#f9fafb"
            }}>
              <h3>AI Analysis</h3>
              <p>{result.ai_analysis}</p>
          </div>

          <div
            style={{
              padding: "24px",
              border: "1px solid #ddd",
              borderRadius: "10px",
              backgroundColor: "#fff",
            }}
          >
            <h3 style={{ marginTop: 0 }}>Reasons</h3>
            {result.reasons && result.reasons.length > 0 ? (
              <ul style={{ marginTop: "12px", paddingLeft: "20px" }}>
                {result.reasons.map((reason, index) => (
                  <li key={index} style={{ marginBottom: "8px" }}>
                    {reason}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No reasons available.</p>
            )}
          </div>

          <div
            style={{
              padding: "24px",
              border: "1px solid #ddd",
              borderRadius: "10px",
              backgroundColor: "#fff",
            }}
          >
            <h3 style={{ marginTop: 0 }}>Recent News</h3>
            {result.news && result.news.length > 0 ? (
              <ul style={{ marginTop: "12px", paddingLeft: "20px" }}>
                {result.news.map((item, index) => (
                  <li key={index} style={{ marginBottom: "14px" }}>
                    <div style={{ fontWeight: "bold", marginBottom: "4px" }}>
                      {item.title}
                    </div>
                    <div style={{ fontSize: "14px", color: "#666" }}>
                      {item.source || "Unknown source"}
                      {item.published_at ? ` - ${item.published_at}` : ""}
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No recent news available.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;