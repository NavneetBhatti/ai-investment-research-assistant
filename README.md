# AI Investment Research Assistant (LangChain + Gemini + RAG)

An AI-powered investment research assistant that analyzes and compares stocks using real-time financial data, deterministic scoring, and Retrieval-Augmented Generation (RAG).

---

## 🚀 Overview

This project combines:
- Real-time financial data (Alpha Vantage)
- Deterministic scoring logic
- AI reasoning using Google Gemini (LangChain)
- Custom knowledge retrieval using RAG (FAISS)

The result is a system that provides **explainable, grounded investment insights** instead of generic AI responses.

---

## 🧠 Key Features

- 📊 Single Stock Analysis (price, fundamentals, news, scoring)
- ⚖️ Compare Two Stocks with AI recommendation
- 🤖 AI explanations using Gemini + LangChain
- 📚 RAG (Retrieval-Augmented Generation) with custom investment rules
- 📉 Scoring system (valuation, trend, sentiment, risk)
- 🛡️ Graceful fallback when APIs fail (no misleading data)
- 📰 News sentiment integration

---

## 🏗️ Architecture

```text
Frontend (React)  
↓  
Backend (FastAPI)  
↓  
--------------------------------  
Alpha Vantage → Market Data APIs  
Gemini (LangChain) → AI reasoning  
FAISS → Vector store (RAG)  
--------------------------------  
↓  
Scoring + Retrieval + LLM Output  

---

## ⚙️ Tech Stack

- Frontend: React (JavaScript)
- Backend: FastAPI (Python)
- AI/LLM: Google Gemini (LangChain)
- RAG: FAISS Vector Store
- Data APIs: Alpha Vantage
- Embeddings: Gemini Embeddings

---

## 🔍 How It Works

1. User inputs stock ticker(s)
2. Backend fetches:
   - Market data
   - Fundamentals
   - News
3. System calculates scores:
   - Valuation
   - Trend
   - News Sentiment
   - Risk
4. RAG retrieves investment rules
5. Gemini generates grounded explanation
6. Results are returned to frontend

---

## 🧠 RAG (Retrieval-Augmented Generation)

Custom investment knowledge is stored as documents and indexed using FAISS.

During analysis:
- Relevant rules are retrieved
- Injected into LLM prompt
- AI responses become more accurate and explainable

---

## ⚖️ Compare Mode

Compare two stocks side-by-side:
- Score breakdown
- AI-generated comparison summary
- Better pick based on scoring logic

---

## 🛡️ Error Handling

- Handles API rate limits gracefully
- Missing data shown as "N/A"
- No fake or misleading values
- Uses "Insufficient Data" fallback mode

---

## ▶️ Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload