import traceback
class SentimentAnalyzerAgent:
    def __init__(self):
        try:
            from transformers import pipeline
            self.model = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        except Exception as e:
            self.model = None

    def analyze(self, headlines):
        if not self.model or not headlines or headlines == ["No news available."]:
            return 0, [{'label': 'NEUTRAL', 'score': 1.0} for _ in (headlines or [""])]
        try:
            sentiments = self.model(headlines)
            score_map = {'POSITIVE': 1, 'NEUTRAL': 0, 'NEGATIVE': -1}
            weighted_score, total_weight = 0, 0
            for sentiment in sentiments:
                confidence = sentiment['score']
                if confidence > 0.7:
                    weight = confidence
                    score = score_map.get(sentiment['label'].upper(), 0)
                    weighted_score += score * weight
                    total_weight += weight
            final_score = weighted_score / total_weight if total_weight > 0 else 0
            return final_score, sentiments
        except:
            return 0, [{'label': 'NEUTRAL', 'score': 1.0} for _ in headlines]
