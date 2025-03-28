from flask import render_template,redirect,url_for,jsonify,request,current_app
from app.api import api_bp
from market_data import get_market_data
from sentiment_analysis import get_news_sentiment
from chatbot import get_chatbot_response
from utils import generate_analysis, get_stock_data
import requests
#from utils import get_market_data, get_news_sentiment
@api_bp.route('/')  # Route for the root URL
def index():
    return redirect(url_for('api.market_data_route', symbol='AAPL'))  # Redirect to market data for AAPL

@api_bp.route('/market_data/<string:symbol>')
def market_data_route(symbol):
    data= get_market_data(symbol)
    if data is None:
        return jsonify({"error":f"Could not retrive market data for {symbol}"}), 404
    return render_template('market_data.html',data=data.to_dict(orient='records'),symbol=symbol)

@api_bp.route('/sentiment_analysis/<string:symbol>')
def sentiment_analysis_route(symbol):
    sentiment= get_news_sentiment(symbol)
    if sentiment is None:
        return jsonify({"error": f"Could not retrieve sentiment analysis for {symbol}"}), 404
    return render_template('sentiment_analysis.html',sentiment=sentiment,symbol=symbol)

@api_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.form['user_message']
        bot_response = get_chatbot_response(user_message)
        return jsonify({'response': bot_response})
    return render_template('chat.html')

@api_bp.route("/analyze", methods=["POST"])
def analyze_finance():
    """API endpoint to analyze financial data."""
    from financial_agent import get_financial_data
    query = "Summarize the stock market trends"
    response = get_financial_data(query)
    return jsonify({"response": response})

@api_bp.route("/playground", methods=["GET"])
def playground_ui():
    """Proxy request to the Playground UI."""
    playground_url = "http://127.0.0.1:9090"
    return requests.get(playground_url)