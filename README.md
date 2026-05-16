# Agentic Stock Analysis Workflow Terminal

Welcome to the **Agentic Stock Analysis Workflow** dashboard! 

> **Important Distinction:** This project is built as a highly deterministic **Agentic AI Workflow**, rather than an open-ended autonomous agent. In institutional finance environments, true autonomous LLM agents (like Auto-GPT) can be unpredictable, slow, and prone to "hallucination loops." To meet professional standards, this tool uses a fixed, robust orchestrator that explicitly routes tasks to specialized sub-agents (Data Collection, FinBERT Sentiment, AI Synthesis, Risk Management). This guarantees fast, strictly formatted, and highly reliable institutional-grade reporting every single time.

This platform provides a robust, multi-agent artificial intelligence framework to analyze stocks from a modern, high-level investor perspective. It leverages the latest data extraction methods, AI-powered CANSLIM evaluation, NLP sentiment analysis, and risk assessment to provide clear, actionable investment decisions synthesized directly by LLMs.

## 🌟 Key Features

- **Agentic Workflow Architecture**: Modular design separating concerns into distinct agents (Data Collector, Fundamental Analyst, Sentiment Analyst, Risk Manager, CANSLIM, and Decision Engine), guided by a master Orchestrator.
- **LLM Synthesis**: Automatically translates complex quantitative metrics into non-technical, layman-readable explanations using advanced language models (via OpenRouter).
- **Comprehensive Data Gathering**: Uses `yfinance` for robust stock market data and technical indicators (SMA), falling back gracefully when APIs are rate-limited.
- **NLP Sentiment Analysis**: Employs FinBERT to gauge market sentiment based on recent headlines, tagging them positively or negatively.
- **Bloomberg Terminal UI Dashboard**: A stunning, dark-themed, data-dense UI built with modern HTML/CSS and interactive Chart.js visualizations that mimics high-end financial terminals.

## 🏗️ Project Structure

The codebase is organized into a robust Python application workflow:

```text
.
├── app.py                      # Main Flask application entry point
├── stock_analyzer/             # Core analysis package
│   ├── orchestrator.py         # Main orchestrator linking all agents and generating synthesis
│   ├── agents/                 # Specialized workflow agents
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
│   └── index.html              # Premium Dark Mode Terminal UI
└── stock_reports/              # Auto-generated analysis history and data dumps
```

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.9+ installed. You'll need the following libraries:

```bash
pip install flask yfinance feedparser pandas numpy transformers torch python-dotenv
```

*(Note: `transformers` and `torch` are used by the FinBERT sentiment analyzer. If they fail to load, the app gracefully falls back to neutral sentiment).*

### Environment Variables

Set your OpenRouter API key inside a `.env` file for advanced CANSLIM analysis and Layman Synthesis:

1. Create a `.env` file in the root directory.
2. Add your key: `OPENROUTER_API_KEY=your-api-key-here`

### Running the App

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
3. Enter a company name (e.g., *Apple Inc.*) and a ticker (e.g., *AAPL*) and click **EXECUTE**.

## 🎨 UI/UX Design Philosophy

The user interface is crafted for professional investors who demand a clean, aesthetic, and incredibly data-dense experience:
- **Terminal Aesthetics**: A stark, black background with `00ff88` (cyber green) and `00b8ff` (cyber blue) accents to highlight critical metrics.
- **Interactive Charting**: Smooth line charts plotted using Chart.js.
- **Transparency**: Every single decision is backed by visible data arrays directly on the dashboard, including FinBERT-tagged news feeds and red/green flagged fundamentals.

## ⚖️ Disclaimer
This tool is for informational and educational purposes only. Always perform your own due diligence before making investment decisions.
