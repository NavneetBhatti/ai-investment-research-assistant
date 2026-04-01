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

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "40px" }}>
      <h1>AI Investment Research Assistant</h1>
      <p>Analyze a stock using a mock backend response.</p>

      <form onSubmit={handleAnalyze} style={{ display: "grid", gap: "16px", marginTop: "24px" }}>
        <div>
          <label>Ticker</label>
          <br />
          <input
            type="text"
            name="ticker"
            value={formData.ticker}
            onChange={handleChange}
            placeholder="e.g. AAPL"
            style={{ width: "100%", padding: "10px", marginTop: "6px" }}
            required
          />
        </div>

        <div>
          <label>Investment Horizon</label>
          <br />
          <select
            name="horizon"
            value={formData.horizon}
            onChange={handleChange}
            style={{ width: "100%", padding: "10px", marginTop: "6px" }}
          >
            <option value="short">Short</option>
            <option value="medium">Medium</option>
            <option value="long">Long</option>
          </select>
        </div>

        <div>
          <label>Risk Level</label>
          <br />
          <select
            name="risk_level"
            value={formData.risk_level}
            onChange={handleChange}
            style={{ width: "100%", padding: "10px", marginTop: "6px" }}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <button type="submit" style={{ padding: "12px 18px", cursor: "pointer" }}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && (
        <div style={{ marginTop: "20px", color: "red" }}>
          {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: "32px", padding: "20px", border: "1px solid #ddd", borderRadius: "8px" }}>
          <h2>{result.ticker} - {result.company_name}</h2>
          <p><strong>Summary:</strong> {result.summary}</p>
          <p><strong>Valuation Score:</strong> {result.valuation_score}</p>
          <p><strong>Trend Score:</strong> {result.trend_score}</p>
          <p><strong>News Score:</strong> {result.news_score}</p>
          <p><strong>Risk Score:</strong> {result.risk_score}</p>
          <p><strong>Recommendation:</strong> {result.recommendation}</p>
          <p><strong>Confidence:</strong> {result.confidence}/10</p>
          <p><strong>Current Price:</strong> {result.current_price || "N/A"}</p>
          <p><strong>Daily Change %:</strong> {result.daily_change_percent || "N/A"}</p>
          <p><strong>P/E Ratio:</strong> {result.pe_ratio || "N/A"}</p>
          <p><strong>EPS:</strong> {result.eps || "N/A"}</p>
          <p><strong>Market Cap:</strong> {result.market_cap || "N/A"}</p>

          <div>
            <strong>Reasons:</strong>
            <ul>
              {result.reasons.map((reason, index) => (
                <li key={index}>{reason}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;