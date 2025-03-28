#import yfinance as yf

def get_market_data(symbol):
    try:
        market_data= get_market_data(symbol)
        if market_data is not None and not  market_data.empty and '4.Close' in market_data.columns:
            last_price=market_data['4.close'].iloc[-1]
            response=f"The current price for {symbol}  is approximately  ${last_price}."
        else:
            response=f"Sorry,I couldnot fetch the price {symbol} at the moment."
    except Exception as e:
             response=f"Error fetching market data: {e}"
    print(response)   
   