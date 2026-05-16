class FundamentalAnalystAgent:
    def __init__(self, company, data_agent):
        self.company = company
        self.data_agent = data_agent

    def comprehensive_analysis(self, financials):
        f = financials or {}
        return {
            'valuation': {
                'pe_ratio': f.get('trailingPE'),
                'pb_ratio': f.get('priceToBook'),
            },
            'profitability': {
                'roe': f.get('returnOnEquity'),
                'roa': f.get('returnOnAssets'),
            },
            'liquidity': {
                'current_ratio': f.get('currentRatio'),
                'quick_ratio': f.get('quickRatio'),
            },
            'leverage': {
                'debt_to_equity': f.get('debtToEquity'),
            },
            'growth': {
                'earnings_quarterly_growth': f.get('earningsQuarterlyGrowth'),
                'earnings_growth': f.get('earningsGrowth'),
                'revenue_growth': f.get('revenueGrowth'),
            },
            'market': {
                'market_cap': f.get('marketCap'),
                'beta': f.get('beta'),
                'institutional_ownership': f.get('heldPercentInstitutions'),
            }
        }
