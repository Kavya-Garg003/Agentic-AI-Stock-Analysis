class DecisionEngineAgent:
    def decide(self, fundamental_analysis, sentiment_score, risk_assessment, canslim_analysis=None):
        total_score = 0
        
        fund_score = self._score_fundamentals(fundamental_analysis)
        total_score += fund_score
        
        canslim_score = (canslim_analysis.get('total_score', 0) / 7) * 30 if canslim_analysis else 0
        total_score += canslim_score
        
        sent_score = max(0, min(15, (sentiment_score + 1) * 7.5))
        total_score += sent_score
        
        risk_score_val = (risk_assessment[0] / risk_assessment[2]) * 15
        total_score += risk_score_val
        
        if total_score >= 70: rec, conf = "BUY", min(0.95, total_score / 100)
        elif total_score >= 50: rec, conf = "HOLD", min(0.85, total_score / 100)
        else: rec, conf = "SELL", max(0.60, total_score / 100)
        
        return {
            'recommendation': rec,
            'total_score': round(total_score, 2),
            'max_score': 100,
            'confidence': round(conf, 3),
            'decision_factors': {
                'fundamental_score': fund_score,
                'canslim_score': canslim_score,
                'sentiment_score': sent_score,
                'risk_score': risk_score_val
            },
            'reasoning': f"Total computed score is {total_score:.2f} out of 100. Fundamentals and sentiment align with a {rec} rating."
        }
        
    def _score_fundamentals(self, analysis):
        score = 20 # Base
        pe = analysis.get('valuation', {}).get('pe_ratio')
        roe = analysis.get('profitability', {}).get('roe')
        
        if pe and 5 <= pe <= 25: score += 10
        if roe and roe > 0.15: score += 10
        return min(40, score)
