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
            financials = data_agent.fetch_financials()
            price_history = data_agent.fetch_price_history()
            market_history = data_agent.fetch_market_index_history()
            headlines = data_agent.fetch_news()
            
            fundamental_analysis = fundamental_agent.comprehensive_analysis(financials)
            report['analysis_results']['fundamental'] = fundamental_analysis
            
            canslim = self.canslim_analyzer.analyze_canslim(company, ticker, financials, price_history, market_history, headlines)
            report['analysis_results']['canslim'] = canslim
            
            sent_score, _ = sentiment_agent.analyze(headlines)
            report['analysis_results']['sentiment'] = {'score': sent_score, 'classification': 'Positive' if sent_score > 0 else 'Negative'}
            
            risk_assessment = risk_agent.assess(financials, price_history)
            report['analysis_results']['risk'] = {'score': risk_assessment[0], 'factors': risk_assessment[1]}
            
            decision = decision_agent.decide(fundamental_analysis, sent_score, risk_assessment, canslim)
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
