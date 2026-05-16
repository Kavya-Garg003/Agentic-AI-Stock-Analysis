import os
import yfinance as yf
import feedparser
import pandas as pd
from urllib.parse import quote_plus
from stock_analyzer.utils.fallback_data import generate_fallback_price_data

class DataCollectorAgent:
    def __init__(self, company, ticker):
        self.company = company
        self.ticker = ticker
        self.report_folder = "stock_reports"
        os.makedirs(self.report_folder, exist_ok=True)

    def fetch_news(self):
        try:
            query = quote_plus(self.company)
            feed_url = f"https://news.google.com/rss/search?q={query}"
            feed = feedparser.parse(feed_url)
            headlines = [entry.title for entry in feed.entries[:15]]
            if not headlines: raise ValueError("No headlines")
            return headlines
        except Exception:
            try:
                df = pd.read_csv(f"{self.report_folder}/{self.ticker}_sentiment.csv")
                return df['Headline'].tolist()
            except:
                return ["No news available."]

    def fetch_company_profile(self):
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            company_officers = info.get('companyOfficers', [])
            ceo = "Unknown"
            if company_officers and len(company_officers) > 0:
                ceo = company_officers[0].get('name', "Unknown")
            
            return {
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'ceo': ceo,
                'website': info.get('website', 'N/A'),
                'summary': info.get('longBusinessSummary', 'No summary available.')
            }
        except:
            return {'sector': 'N/A', 'industry': 'N/A', 'ceo': 'Unknown', 'website': 'N/A', 'summary': 'Data unavailable.'}

    def fetch_financials(self):
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            # Fallback for missing keys in yfinance by returning dict with defaults
            financials = {
                'currentPrice': info.get('currentPrice', info.get('regularMarketPrice')),
                'trailingPE': info.get('trailingPE', 0),
                'forwardPE': info.get('forwardPE', 0),
                'priceToBook': info.get('priceToBook', 0),
                'trailingEps': info.get('trailingEps', 0),
                'returnOnEquity': info.get('returnOnEquity', 0),
                'returnOnAssets': info.get('returnOnAssets', 0),
                'debtToEquity': info.get('debtToEquity', 0),
                'currentRatio': info.get('currentRatio', 1),
                'quickRatio': info.get('quickRatio', 1),
                'beta': info.get('beta', 1),
                'earningsQuarterlyGrowth': info.get('earningsQuarterlyGrowth', 0),
                'earningsGrowth': info.get('earningsGrowth', 0),
                'revenueGrowth': info.get('revenueGrowth', 0),
                'volume': info.get('volume', 0),
                'marketCap': info.get('marketCap', 0),
                'heldPercentInstitutions': info.get('heldPercentInstitutions', 0)
            }
            if financials['currentPrice'] is None: raise ValueError("Incomplete data")
            return financials
        except Exception:
            try:
                df = pd.read_csv(f"{self.report_folder}/{self.ticker}_financials.csv")
                return df.iloc[0].to_dict()
            except:
                return {'currentPrice': 100, 'trailingPE': 15, 'returnOnEquity': 0.15, 'debtToEquity': 50, 'currentRatio': 1.5, 'beta': 1.1, 'earningsGrowth': 0.10, 'marketCap': 1e9}

    def fetch_price_history(self, period="3mo"):
        try:
            stock = yf.Ticker(self.ticker)
            df = stock.history(period=period)
            if df.empty: raise ValueError("Empty")
            # Calculate basic technicals
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()
            return df
        except:
            return generate_fallback_price_data()

    def fetch_market_index_history(self, index_ticker="^GSPC", period="3mo"):
        try:
            index = yf.Ticker(index_ticker)
            df = index.history(period=period)
            if df.empty: return generate_fallback_price_data(days=63)
            return df
        except:
            return generate_fallback_price_data(days=63)
