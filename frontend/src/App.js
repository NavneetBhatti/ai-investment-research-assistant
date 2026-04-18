import { useState } from "react";

function App() {
  const [mode, setMode] = useState("single");

  const [singleFormData, setSingleFormData] = useState({
    ticker: "",
    horizon: "medium",
    risk_level: "medium",
  });

  const [compareFormData, setCompareFormData] = useState({
    ticker_1: "",
    ticker_2: "",
    horizon: "medium",
    risk_level: "medium",
  });

  const [singleResult, setSingleResult] = useState(null);
  const [compareResult, setCompareResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const cardStyle = {
    padding: "24px",
    border: "1px solid #ddd",
    borderRadius: "10px",
    backgroundColor: "#fff",
  };

  const metricCardStyle = {
    padding: "14px",
    border: "1px solid #eee",
    borderRadius: "8px",
  };

  const inputStyle = {
    width: "100%",
    padding: "10px",
    marginTop: "6px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    boxSizing: "border-box",
  };

  const getScoreDisplay = (value) => {
    return value !== null && value !== undefined ? `${value}/10` : "N/A";
  };

  const getSentimentStyle = (sentiment) => {
    const normalized = (sentiment || "").toLowerCase();

    if (normalized.includes("positive")) {
      return { color: "green", label: "🟢 Positive" };
    }

    if (normalized.includes("negative")) {
      return { color: "red", label: "🔴 Negative" };
    }

    if (normalized.includes("neutral")) {
      return { color: "#666", label: "⚪ Neutral" };
    }

    return { color: "#666", label: sentiment || "N/A" };
  };

  const handleSingleChange = (event) => {
    const { name, value } = event.target;
    setSingleFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCompareChange = (event) => {
    const { name, value } = event.target;
    setCompareFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSingleAnalyze = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setSingleResult(null);
    setCompareResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(singleFormData),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch single stock analysis");
      }

      const data = await response.json();
      setSingleResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleCompareAnalyze = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setSingleResult(null);
    setCompareResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/compare", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(compareFormData),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch comparison analysis");
      }

      const data = await response.json();
      setCompareResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const renderSingleResult = (result) => {
    const sentimentDisplay = getSentimentStyle(result?.news_sentiment);

    return (
      <div style={{ marginTop: "32px", display: "grid", gap: "20px" }}>
        <div style={cardStyle}>
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
            <div style={metricCardStyle}>
              <strong>Valuation Score</strong>
              <div style={{ marginTop: "8px", fontSize: "24px" }}>
                {getScoreDisplay(result.valuation_score)}
              </div>
            </div>

            <div style={metricCardStyle}>
              <strong>Trend Score</strong>
              <div style={{ marginTop: "8px", fontSize: "24px" }}>
                {getScoreDisplay(result.trend_score)}
              </div>
            </div>

            <div style={metricCardStyle}>
              <strong>News Score</strong>
              <div style={{ marginTop: "8px", fontSize: "24px" }}>
                {getScoreDisplay(result.news_score)}
              </div>
            </div>

            <div style={metricCardStyle}>
              <strong>Risk Score</strong>
              <div style={{ marginTop: "8px", fontSize: "24px" }}>
                {getScoreDisplay(result.risk_score)}
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
            <div style={metricCardStyle}>
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

            <div style={metricCardStyle}>
              <strong>Recommendation</strong>
              <div style={{ marginTop: "8px", fontSize: "20px", fontWeight: "bold" }}>
                {result.recommendation || "N/A"}
              </div>
            </div>

            <div style={metricCardStyle}>
              <strong>Confidence</strong>
              <div style={{ marginTop: "8px", fontSize: "20px", fontWeight: "bold" }}>
                {getScoreDisplay(result.confidence)}
              </div>
            </div>
          </div>
        </div>

        <div style={cardStyle}>
          <h3 style={{ marginTop: 0 }}>Details</h3>
          <p><strong>Current Price:</strong> {result.current_price || "N/A"}</p>
          <p><strong>Daily Change %:</strong> {result.daily_change_percent || "N/A"}</p>
          <p><strong>P/E Ratio:</strong> {result.pe_ratio || "N/A"}</p>
          <p><strong>EPS:</strong> {result.eps || "N/A"}</p>
          <p><strong>Market Cap:</strong> {result.market_cap || "N/A"}</p>
        </div>

        <div style={{ ...cardStyle, backgroundColor: "#f9fafb" }}>
          <h3 style={{ marginTop: 0 }}>AI Analysis</h3>
          <p style={{ marginTop: "12px", lineHeight: "1.6" }}>
            {result.ai_analysis || "No AI analysis available."}
          </p>
        </div>

        <div style={cardStyle}>
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

        <div style={cardStyle}>
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
    );
  };

  const renderCompareStockCard = (stock) => {
    const sentimentDisplay = getSentimentStyle(stock?.news_sentiment);

    return (
      <div style={cardStyle}>
        <h2 style={{ marginTop: 0 }}>
          {stock.ticker} - {stock.company_name}
        </h2>

        <p style={{ color: "#555" }}>{stock.summary}</p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, minmax(120px, 1fr))",
            gap: "12px",
            marginTop: "18px",
          }}
        >
          <div style={metricCardStyle}>
            <strong>Valuation</strong>
            <div style={{ marginTop: "8px", fontSize: "20px" }}>
              {getScoreDisplay(stock.valuation_score)}
            </div>
          </div>

          <div style={metricCardStyle}>
            <strong>Trend</strong>
            <div style={{ marginTop: "8px", fontSize: "20px" }}>
              {getScoreDisplay(stock.trend_score)}
            </div>
          </div>

          <div style={metricCardStyle}>
            <strong>News</strong>
            <div style={{ marginTop: "8px", fontSize: "20px" }}>
              {getScoreDisplay(stock.news_score)}
            </div>
          </div>

          <div style={metricCardStyle}>
            <strong>Risk</strong>
            <div style={{ marginTop: "8px", fontSize: "20px" }}>
              {getScoreDisplay(stock.risk_score)}
            </div>
          </div>
        </div>

        <div
          style={{
            marginTop: "18px",
            display: "grid",
            gap: "10px",
          }}
        >
          <div><strong>Recommendation:</strong> {stock.recommendation || "N/A"}</div>
          <div><strong>Confidence:</strong> {getScoreDisplay(stock.confidence)}</div>
          <div>
            <strong>News Sentiment:</strong>{" "}
            <span style={{ color: sentimentDisplay.color }}>{sentimentDisplay.label}</span>
          </div>
          <div><strong>Current Price:</strong> {stock.current_price || "N/A"}</div>
          <div><strong>Daily Change %:</strong> {stock.daily_change_percent || "N/A"}</div>
          <div><strong>P/E Ratio:</strong> {stock.pe_ratio || "N/A"}</div>
          <div><strong>EPS:</strong> {stock.eps || "N/A"}</div>
          <div><strong>Market Cap:</strong> {stock.market_cap || "N/A"}</div>
        </div>

        <div style={{ marginTop: "18px" }}>
          <strong>AI Analysis</strong>
          <p style={{ marginTop: "8px", lineHeight: "1.5" }}>
            {stock.ai_analysis || "No AI analysis available."}
          </p>
        </div>
      </div>
    );
  };

  return (
    <div
      style={{
        maxWidth: "1100px",
        margin: "0 auto",
        padding: "40px 20px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1 style={{ marginBottom: "8px" }}>AI Investment Research Assistant</h1>
      <p style={{ color: "#555", marginTop: 0 }}>
        Analyze one stock or compare two stocks using live data, scoring, Gemini, and RAG.
      </p>

      <div
        style={{
          display: "flex",
          gap: "12px",
          marginTop: "20px",
          marginBottom: "24px",
        }}
      >
        <button
          onClick={() => {
            setMode("single");
            setError("");
            setCompareResult(null);
          }}
          style={{
            padding: "10px 16px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            backgroundColor: mode === "single" ? "#111" : "#fff",
            color: mode === "single" ? "#fff" : "#111",
            cursor: "pointer",
          }}
        >
          Single Analysis
        </button>

        <button
          onClick={() => {
            setMode("compare");
            setError("");
            setSingleResult(null);
          }}
          style={{
            padding: "10px 16px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            backgroundColor: mode === "compare" ? "#111" : "#fff",
            color: mode === "compare" ? "#fff" : "#111",
            cursor: "pointer",
          }}
        >
          Compare Two Stocks
        </button>
      </div>

      {mode === "single" && (
        <form
          onSubmit={handleSingleAnalyze}
          style={{
            display: "grid",
            gap: "16px",
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
              value={singleFormData.ticker}
              onChange={handleSingleChange}
              placeholder="e.g. AAPL"
              style={inputStyle}
              required
            />
          </div>

          <div>
            <label><strong>Investment Horizon</strong></label>
            <br />
            <select
              name="horizon"
              value={singleFormData.horizon}
              onChange={handleSingleChange}
              style={inputStyle}
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
              value={singleFormData.risk_level}
              onChange={handleSingleChange}
              style={inputStyle}
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
      )}

      {mode === "compare" && (
        <form
          onSubmit={handleCompareAnalyze}
          style={{
            display: "grid",
            gap: "16px",
            padding: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            backgroundColor: "#fafafa",
          }}
        >
          <div>
            <label><strong>First Ticker</strong></label>
            <br />
            <input
              type="text"
              name="ticker_1"
              value={compareFormData.ticker_1}
              onChange={handleCompareChange}
              placeholder="e.g. AAPL"
              style={inputStyle}
              required
            />
          </div>

          <div>
            <label><strong>Second Ticker</strong></label>
            <br />
            <input
              type="text"
              name="ticker_2"
              value={compareFormData.ticker_2}
              onChange={handleCompareChange}
              placeholder="e.g. MSFT"
              style={inputStyle}
              required
            />
          </div>

          <div>
            <label><strong>Investment Horizon</strong></label>
            <br />
            <select
              name="horizon"
              value={compareFormData.horizon}
              onChange={handleCompareChange}
              style={inputStyle}
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
              value={compareFormData.risk_level}
              onChange={handleCompareChange}
              style={inputStyle}
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
            {loading ? "Comparing..." : "Compare"}
          </button>
        </form>
      )}

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

      {singleResult && renderSingleResult(singleResult)}

      {compareResult && (
        <div style={{ marginTop: "32px", display: "grid", gap: "20px" }}>
          <div
            style={{
              padding: "18px 24px",
              border: "1px solid #ddd",
              borderRadius: "10px",
              backgroundColor: "#f9fafb",
            }}
          >
            <h2 style={{ marginTop: 0, marginBottom: "8px" }}>Comparison Result</h2>
            <p style={{ margin: 0 }}>
              <strong>Better Pick:</strong> {compareResult.better_pick || "N/A"}
            </p>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
              gap: "20px",
            }}
          >
            {renderCompareStockCard(compareResult.stock_1)}
            {renderCompareStockCard(compareResult.stock_2)}
          </div>

          <div style={{ ...cardStyle, backgroundColor: "#f9fafb" }}>
            <h3 style={{ marginTop: 0 }}>AI Comparison Summary</h3>
            <p style={{ marginTop: "12px", lineHeight: "1.6" }}>
              {compareResult.comparison_summary || "No comparison summary available."}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;