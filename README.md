# Premium Agentic AI Stock Analysis

Welcome to the **Agentic AI Stock Analysis** dashboard! This project provides a robust, multi-agent artificial intelligence framework to analyze stocks from a modern, high-level investor perspective. It leverages the latest data extraction methods, AI-powered CANSLIM evaluation, sentiment analysis, and risk assessment to provide clear, actionable investment decisions.

## 🌟 Key Features

- **Multi-Agent Architecture**: Modular design separating concerns into distinct agents (Data Collector, Fundamental Analyst, Sentiment Analyst, Risk Manager, CANSLIM, and Decision Engine).
- **Comprehensive Data Gathering**: Uses `yfinance` for robust stock market data and technical indicators (SMA), falling back gracefully when APIs are rate-limited.
- **AI CANSLIM Analysis**: Uses LLMs (via OpenRouter) to automatically score the stock based on William O'Neil's legendary CANSLIM strategy.
- **NLP Sentiment Analysis**: Employs FinBERT to gauge market sentiment based on recent headlines.
- **Premium UI Dashboard**: A stunning, dark-themed, glassmorphism UI built with modern HTML/CSS and interactive Chart.js visualizations.
- **Resilient Engine**: Safely falls back to local data and computed heuristics if external APIs are unavailable.

## 🏗️ Project Structure

The codebase has been refactored from a monolithic Jupyter Notebook into a robust Python application:

```text
.
├── app.py                      # Main Flask application entry point
├── stock_analyzer/             # Core analysis package
│   ├── orchestrator.py         # Main orchestrator linking all agents
│   ├── agents/                 # Specialized AI agents
│   │   ├── canslim.py          # LLM-powered CANSLIM analyzer
│   │   ├── data_collector.py   # yfinance and news fetcher
│   │   ├── decision.py         # Final scoring and recommendation engine
│   │   ├── fundamental.py      # Core financial metrics evaluation
│   │   ├── risk.py             # Volatility, liquidity, and debt assessment
│   │   └── sentiment.py        # FinBERT news sentiment analyzer
│   └── utils/                  # Helper utilities
│       ├── fallback_data.py    # Fallback data generator
│       └── persistence.py      # Saves analysis to stock_reports/
├── templates/                  
│   └── index.html              # Premium Dark Mode Dashboard UI
└── stock_reports/              # Auto-generated analysis history and data dumps
```

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.9+ installed. You'll need the following libraries:

```bash
pip install flask yfinance feedparser pandas numpy transformers torch
```

*(Note: `transformers` and `torch` are used by the FinBERT sentiment analyzer. If they fail to load, the app gracefully falls back to neutral sentiment).*

### Environment Variables

Set your OpenRouter API key for advanced CANSLIM analysis:

```bash
# Windows (PowerShell)
$env:OPENROUTER_API_KEY="your-api-key"

# Linux/Mac
export OPENROUTER_API_KEY="your-api-key"
```

### Running the App

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
3. Enter a company name (e.g., *NVIDIA Corp*) and a ticker (e.g., *NVDA*) and click **Analyze Asset**.

## 🎨 UI/UX Design Philosophy

The user interface is crafted for professional investors who demand a clean, aesthetic, and responsive experience. It features:
- **Neon Accents**: A `00ff88` (cyber green) and `00b8ff` (cyber blue) color scheme to highlight important metrics.
- **Interactive Charting**: Smooth line charts plotted using Chart.js with dynamic gradients.
- **Score Dashboards**: Quick-glance cards showing fundamental score, risk metrics, sentiment, and the final aggregate confidence score out of 100.

## ⚖️ Disclaimer
This tool is for informational and educational purposes only. Always perform your own due diligence before making investment decisions.
