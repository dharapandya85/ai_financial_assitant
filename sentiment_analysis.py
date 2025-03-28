import os
import newsapi
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_news_sentiment(symbol):
    newsapi_key= os.getenv("NEWS_API_KEY")
    newsapi_client= newsapi.NewsApiClient(api_key=newsapi_key)
    articles= newsapi_client.get_everything(q=symbol,language="en")["articles"]
    analyzer=SentimentIntensityAnalyzer()
    sentiments=[analyzer.polarity_scores(article["title"])["compound"] for article in articles]
    average_sentiment=sum(sentiments)/len(sentiments) if sentiments else 0
    return average_sentiment