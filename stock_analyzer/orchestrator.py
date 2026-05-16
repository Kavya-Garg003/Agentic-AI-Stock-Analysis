from datetime import datetime
from stock_analyzer.agents.data_collector import DataCollectorAgent
from stock_analyzer.agents.fundamental import FundamentalAnalystAgent
from stock_analyzer.agents.sentiment import SentimentAnalyzerAgent
from stock_analyzer.agents.risk import RiskManagerAgent
from stock_analyzer.agents.canslim import CANSLIMAnalyzer
from stock_analyzer.agents.decision import DecisionEngineAgent
from stock_analyzer.utils.persistence import DataPersistenceManager

class StockAnalysisOrchestrator:
    def __init__(self, openrouter_api_key=None):
        self.api_key = openrouter_api_key
        self.canslim_analyzer = CANSLIMAnalyzer(openrouter_api_key)

    def analyze_stock(self, company, ticker):
        data_agent = DataCollectorAgent(company, ticker)
        fundamental_agent = FundamentalAnalystAgent(company, data_agent)
        sentiment_agent = SentimentAnalyzerAgent()
        risk_agent = RiskManagerAgent()
        decision_agent = DecisionEngineAgent()
        persistence = DataPersistenceManager(ticker)
        
        report = {'company': company, 'ticker': ticker, 'analysis_date': datetime.now().isoformat(), 'analysis_results': {}}
        
        try:
            profile = data_agent.fetch_company_profile()
            report['company_profile'] = profile

            financials = data_agent.fetch_financials()
            price_history = data_agent.fetch_price_history()
            market_history = data_agent.fetch_market_index_history()
            headlines = data_agent.fetch_news()
            
            fundamental_analysis = fundamental_agent.comprehensive_analysis(financials)
            report['analysis_results']['fundamental'] = fundamental_analysis
            
            canslim = self.canslim_analyzer.analyze_canslim(company, ticker, financials, price_history, market_history, headlines)
            report['analysis_results']['canslim'] = canslim
            
            sent_score, detailed_sentiments = sentiment_agent.analyze(headlines)
            
            # Combine headlines with their sentiment
            news_feed = []
            for i, hl in enumerate(headlines):
                if i < len(detailed_sentiments):
                    news_feed.append({'headline': hl, 'label': detailed_sentiments[i]['label']})
            
            report['analysis_results']['sentiment'] = {'score': sent_score, 'classification': 'Positive' if sent_score > 0 else 'Negative', 'news_feed': news_feed}
            
            risk_assessment = risk_agent.assess(financials, price_history)
            report['analysis_results']['risk'] = {'score': risk_assessment[0], 'factors': risk_assessment[1]}
            
            decision = decision_agent.decide(fundamental_analysis, sent_score, risk_assessment, canslim)
            
            # Agentic Synthesis: Layman's explanation
            layman_explanation = f"We suggest a {decision['recommendation']} for {company}."
            reasoning_list = []
            if fundamental_analysis.get('valuation', {}).get('pe_ratio', 0) > 40: reasoning_list.append(f"its valuation is very high (P/E > 40)")
            elif fundamental_analysis.get('valuation', {}).get('pe_ratio', 0) < 15: reasoning_list.append(f"it is currently undervalued")
            if sent_score < -0.1: reasoning_list.append("the news has been mostly negative lately")
            elif sent_score > 0.1: reasoning_list.append("there is strong positive news sentiment")
            if risk_assessment[0] <= 3: reasoning_list.append("there are high financial risks such as debt or volatility")
            
            if reasoning_list:
                layman_explanation += f" This is primarily because " + " and ".join(reasoning_list) + "."
            else:
                layman_explanation += " The fundamentals and market trends are currently stable but mixed."
                
            # If we have the API, let the LLM make it sound completely human
            if self.api_key and not self.api_key.startswith("sk-or-v1-8fa"):
                import requests
                prompt = f"Explain to a non-technical person why we are recommending to {decision['recommendation']} {company} stock. Mention that its P/E ratio is {fundamental_analysis.get('valuation', {}).get('pe_ratio')}, news sentiment is {'positive' if sent_score > 0 else 'negative'}, and risk is {risk_assessment[0]}/10. Keep it to one or two simple, professional sentences."
                try:
                    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]}, timeout=15)
                    if res.status_code == 200:
                        layman_explanation = res.json()['choices'][0]['message']['content'].strip()
                except:
                    pass

            decision['layman_explanation'] = layman_explanation
            report['analysis_results']['final_decision'] = decision
            
            # Additional chart data for UI
            # Extract just close prices for simple charting
            if not price_history.empty:
                # Get last 30 days of closes
                last_30_dates = price_history.index[-30:].strftime('%Y-%m-%d').tolist()
                last_30_closes = price_history['Close'].iloc[-30:].tolist()
                report['chart_data'] = {'dates': last_30_dates, 'prices': last_30_closes}
            
            persistence.save_analysis_report(report)
            return report
        except Exception as e:
            report['error'] = str(e)
            return report
