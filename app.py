from flask import Flask, request, jsonify, render_template
from stock_analyzer.orchestrator import StockAnalysisOrchestrator
import os
from dotenv import load_dotenv

load_dotenv()

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

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    ticker = data.get('ticker', '').upper()
    question = data.get('question', '')
    
    if not ticker or not question:
        return jsonify({"error": "Missing ticker or question"}), 400
        
    if not API_KEY or API_KEY.startswith("sk-or-v1-8fa"):
        return jsonify({"answer": "OpenRouter API key is missing. I cannot answer queries without it."})
        
    try:
        import json, requests
        with open(f"stock_reports/{ticker}_analysis_report.json", "r") as f:
            report_data = json.load(f)
            
        prompt = f"You are a financial AI assistant. Based strictly on the following analysis report for {ticker}, answer the user's question concisely. If the answer is not in the data, state that you don't know based on the provided report.\n\nREPORT DATA: {json.dumps(report_data)}\n\nUSER QUESTION: {question}"
        
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, 
            json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3},
            timeout=15
        )
        if res.status_code == 200:
            answer = res.json()['choices'][0]['message']['content'].strip()
            return jsonify({"answer": answer})
        else:
            return jsonify({"error": "Failed to query LLM"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
