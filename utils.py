import os
import openai
import time
import random
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_stock_data(symbol):
  ts= TimeSeries(key=alpha_vantage_api_key, output_format='pandas')
  try:
    data, meta_data= ts.get_daily(symbol, outputsize="compact")
    return data
  except Exception as e:
    print(f"Error fetching stock data for {symbol}:{e}")
    return None

def generate_analysis(symbol, data):
    """Generates analysis using OpenAI."""
    prompt = f"Analyze the following stock data for {symbol}:\n\n{data.to_string()}\n\nProvide insights on trends, potential risks, and opportunities."
    
     # Create a text generation pipeline using a suitable model
    generator = pipeline("text-generation", model="facebook/opt-125m")  # You can choose other models as well

    max_retries = 3  # Adjust as needed
    retry_delay = 1  
    # Initial delay in seconds  # adjust for creativity
    for attempt in range(max_retries):
        try:
            stock_data=get_stock_data(symbol)
            if stock_data is not None:
              analysis_result =generate_analysis(symbol,stock_data)
            else:
              analysis_result="Stock data not available"
            generated_text = generator(prompt, max_length=200, num_return_sequences=1,truncation=True)
            analysis = generated_text[0]['generated_text'].strip()
            return analysis  # Return analysis if successful
        except Exception as e:  # Catch potential errors during text generation
            if "Rate limit" in str(e):  # Check for rate limit errors
                print(f"Rate limit hit, retrying in {retry_delay} seconds (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= random.uniform(1.5, 2.5)  # Exponential backoff
            else:
                raise e  # Re-raise other exceptio
    
    raise Exception("Error during text generation after multiple retries")
