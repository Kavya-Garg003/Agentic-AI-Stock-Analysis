from flask import Flask, request, jsonify, render_template
from stock_analyzer.orchestrator import StockAnalysisOrchestrator
import os

app = Flask(__name__)
API_KEY = os.getenv("OPENROUTER_API_KEY", "")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['GET'])
def analyze():
    company = request.args.get('company')
    ticker = request.args.get('ticker')
    if not company or not ticker:
        return jsonify({"error": "Missing company or ticker"}), 400
        
    orch = StockAnalysisOrchestrator(API_KEY)
    res = orch.analyze_stock(company, ticker.upper())
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
