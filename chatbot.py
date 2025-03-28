import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import random
#from app import generate_analysis, get_stock_data
from market_data import get_market_data
from sentiment_analysis import get_news_sentiment
from utils import generate_analysis, get_stock_data
try:
    nltk.data.find('corpora/wordnet')
except Exception as e:
    print(f"Error downloading WordNet data :{e}")
    nltk.download('wordnet')

try:
    nltk.data.find('punkt')
except Exception as e:
    print(f"Error dwonloading Punkt data :{e}")
    nltk.download('punkt')

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower()) # Remove punctuation and lowercase
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(lemmatized_tokens)

def get_chatbot_response(user_input):
    processed_input = preprocess_text(user_input)
    response = "I'm sorry, I didn't understand your request."

    if "price" in processed_input and ("stock" in processed_input or "AAPL" in processed_input or "GOOG" in processed_input):
        # Basic intent recognition for price
        symbol = "AAPL"  # Default or you can try to extract the symbol
        market_data = get_market_data(symbol)
        try:
            market_data= get_market_data(symbol)
            if market_data is not None:
                last_price = market_data['4. close'].iloc[-1] if '4. close' in market_data.columns and not market_data.empty else "N/A"
                response = f"The current price for {symbol} is approximately ${last_price}."
            else:
                response = f"Sorry, I couldn't fetch the price for {symbol} at the moment."
        except Exception as e:
            response= f"Fetching the current price for {symbol}..." # You'll need to call your get_market_data function here
            print("Error fetching market data:{e}")

    elif "sentiment" in processed_input and ("stock" in processed_input or "Tesla" in processed_input):
        symbol = "TSLA"
        try:
            sentiment = get_news_sentiment(symbol)
            if sentiment is not None:
                if sentiment > 0.1:
                    response = f"The sentiment for news about {symbol} is positive ({sentiment:.2f})."
                elif sentiment < -0.1:
                    response = f"The sentiment for news about {symbol} is negative ({sentiment:.2f})."
                else:
                    response = f"The sentiment for news about {symbol} is neutral ({sentiment:.2f})."
            else:
        
               response = f"Sorry, I couldn't analyze the sentiment for {symbol} at the moment."
        except Exception as e:
            response= f"Analyzing the sentiment for {symbol}..." # You'll need to call get_news_sentiment
            print(f"Error analyzing sentiment: {e}")
    elif "analysis" in processed_input and ("stock" in processed_input or "Google" in processed_input):
        symbol = "GOOG"
        try:
            analysis_result = generate_analysis(symbol, get_stock_data(symbol)) # Assuming you have this
            if analysis_result:
                response = f"Analysis for {symbol}: {analysis_result}"
            else:
                response = f"Sorry, I couldn't generate an analysis for {symbol}."  
        except Exception as e:
            response = f"Error generating analysis: {e}"
            print(f"Error generating analysis: {e}")       
        #response= f"Generating an analysis for {symbol}..." # You'll need to call generate_analysis

    elif "hello" in processed_input or "hi" in processed_input:
        response= random.choice(["Hello!", "Hi there!", "Greetings!"])

    else:
        return "I'm sorry, I didn't understand your request. Please ask about stock prices, sentiment, or analysis."

if __name__ == '__main__':
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            response = get_chatbot_response(user_input)
            print("Bot:", response)
        except Exception as e:
            print(f'Error :{e}')
