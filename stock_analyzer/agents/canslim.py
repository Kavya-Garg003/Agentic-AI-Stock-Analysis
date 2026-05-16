import requests
import json

class CANSLIMAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def analyze_canslim(self, company, ticker, financials, price_history, market_history, news_headlines):
        if not self.api_key or self.api_key.startswith("sk-or-v1-8fa"):
            return self._fallback_canslim_analysis(financials, price_history, market_history, news_headlines)
        
        prompt = f"Analyze {company} ({ticker}) using CANSLIM methodology. Provide score out of 7. Respond in strict JSON. ..."
        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
            res = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            if res.status_code == 200:
                content = res.json()['choices'][0]['message']['content']
                if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
                return json.loads(content)
        except:
            pass
        return self._fallback_canslim_analysis(financials, price_history, market_history, news_headlines)

    def _fallback_canslim_analysis(self, financials, price_history, market_history, news_headlines):
        f = financials or {}
        scores = {}
        # C
        qg = f.get('earningsQuarterlyGrowth', 0) or 0
        scores['C'] = {"score": 1 if qg > 0.25 else 0, "reasoning": f"Q Growth {qg*100:.1f}%"}
        # A
        ag = f.get('earningsGrowth', 0) or 0
        scores['A'] = {"score": 1 if ag > 0.25 else 0, "reasoning": f"Ann Growth {ag*100:.1f}%"}
        # N
        n_score = 1 if any('new' in h.lower() for h in (news_headlines or [])) else 0
        scores['N'] = {"score": n_score, "reasoning": "New catalysts found" if n_score else "No new catalysts"}
        # S
        scores['S'] = {"score": 1, "reasoning": "Assumed solid volume"}
        # L
        scores['L'] = {"score": 1, "reasoning": "Assumed outperforming"}
        # I
        inst = f.get('heldPercentInstitutions', 0) or 0
        scores['I'] = {"score": 1 if inst > 0.3 else 0, "reasoning": f"Inst Ownership {inst*100:.1f}%"}
        # M
        scores['M'] = {"score": 1, "reasoning": "Assumed positive market"}
        
        total = sum(i['score'] for i in scores.values())
        return {
            "canslim_analysis": scores,
            "total_score": total,
            "recommendation": "BUY" if total >= 5 else "HOLD" if total >= 3 else "SELL",
            "risk_level": "LOW" if total >= 5 else "HIGH",
            "confidence": min(0.9, total/7),
            "key_strengths": ["Earnings Growth"] if total > 3 else [],
            "key_weaknesses": ["Slow Growth"] if total < 3 else [],
            "summary": f"Fallback CANSLIM Score {total}/7"
        }
