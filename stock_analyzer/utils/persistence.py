import os
import json
import pandas as pd

class DataPersistenceManager:
    def __init__(self, ticker):
        self.ticker = ticker
        self.report_folder = "stock_reports"
        os.makedirs(self.report_folder, exist_ok=True)

    def save_financials(self, financials):
        try:
            pd.DataFrame([financials]).to_csv(f"{self.report_folder}/{self.ticker}_financials.csv", index=False)
        except Exception as e: print(f"Error saving financials: {e}")

    def save_price_history(self, price_history):
        try:
            price_history.to_csv(f"{self.report_folder}/{self.ticker}_prices.csv")
        except Exception as e: print(f"Error saving price history: {e}")

    def save_news_sentiment(self, headlines, sentiment_results):
        try:
            df = pd.DataFrame({'Headline': headlines, 'Sentiment': [s.get('label', 'N') for s in sentiment_results], 'Confidence': [s.get('score', 0.0) for s in sentiment_results]})
            df.to_csv(f"{self.report_folder}/{self.ticker}_sentiment.csv", index=False)
        except Exception as e: print(f"Error saving sentiment data: {e}")

    def save_analysis_report(self, analysis_report):
        try:
            with open(f"{self.report_folder}/{self.ticker}_analysis_report.json", 'w') as f:
                json.dump(analysis_report, f, indent=2, default=str)
        except Exception as e: print(f"Error saving analysis report: {e}")
