import numpy as np
class RiskManagerAgent:
    def assess(self, financials, price_history):
        f = financials or {}
        risk_factors = {}
        risk_score = 0
        max_score = 10
        
        # Debt
        de = f.get('debtToEquity', 100)
        if de is not None:
            if de < 50: risk_score += 1; risk_factors['debt_level'] = 'Low'
            elif de < 100: risk_factors['debt_level'] = 'Moderate'
            else: risk_factors['debt_level'] = 'High'
            
        # Liquidity
        cr = f.get('currentRatio', 1.0)
        if cr is not None:
            if cr > 1.5: risk_score += 1; risk_factors['liquidity'] = 'Good'
            elif cr > 1.0: risk_factors['liquidity'] = 'Adequate'
            else: risk_factors['liquidity'] = 'Poor'
            
        # Beta
        b = f.get('beta', 1.5)
        if b is not None:
            if b < 1.2: risk_score += 1; risk_factors['market_risk'] = 'Low'
            elif b < 1.5: risk_factors['market_risk'] = 'Moderate'
            else: risk_factors['market_risk'] = 'High'
            
        # Profitability
        roe = f.get('returnOnEquity', 0)
        if roe is not None:
            if roe > 0.15: risk_score += 1; risk_factors['profitability'] = 'Strong'
            elif roe > 0.10: risk_factors['profitability'] = 'Adequate'
            else: risk_factors['profitability'] = 'Weak'
            
        # Volatility
        try:
            if not price_history.empty and len(price_history) > 30:
                volatility = price_history['Close'].pct_change().dropna().std() * np.sqrt(252)
                if volatility < 0.20: risk_score += 1; risk_factors['volatility'] = 'Low'
                elif volatility < 0.35: risk_factors['volatility'] = 'Moderate'
                else: risk_factors['volatility'] = 'High'
            else:
                risk_factors['volatility'] = 'Unknown'
        except:
            risk_factors['volatility'] = 'Unknown'
            
        # Technical Indicator Risk (new)
        try:
            if 'SMA_20' in price_history.columns and 'SMA_50' in price_history.columns:
                last_20 = price_history['SMA_20'].iloc[-1]
                last_50 = price_history['SMA_50'].iloc[-1]
                if last_20 > last_50: risk_score += 1; risk_factors['trend'] = 'Positive'
                else: risk_factors['trend'] = 'Negative'
        except:
            pass

        return risk_score, risk_factors, max_score
