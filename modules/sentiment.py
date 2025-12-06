from textblob import TextBlob
import yfinance as yf

def get_ticker_news_sentiment(ticker_symbol):
    """
    Fetches news for a single ticker and calculates average sentiment.
    Returns:
        float: Average polarity (-1 to 1).
        list: List of headlines used.
    """
    print(f"DEBUG: Fetching news for {ticker_symbol}...")
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        
        if not news:
            print(f"DEBUG: No news found for {ticker_symbol}")
            return 0.0, []
        
        sentiments = []
        headlines = []
        
        for item in news:
            title = item.get('title', '')
            if title:
                blob = TextBlob(title)
                sentiments.append(blob.sentiment.polarity)
                headlines.append(title)
                
        if not sentiments:
            print(f"DEBUG: No valid headlines for {ticker_symbol}")
            return 0.0, []
            
        avg_sentiment = sum(sentiments) / len(sentiments)
        print(f"DEBUG: {ticker_symbol} Sentiment: {avg_sentiment:.4f} (based on {len(sentiments)} headlines)")
        return avg_sentiment, headlines
        
    except Exception as e:
        print(f"ERROR: Failed to fetch news for {ticker_symbol}: {e}")
        return 0.0, []

def get_market_sentiment(tickers):
    """
    Gets sentiment for a list of tickers.
    
    Returns:
        dict: {ticker: {'score': float, 'headlines': list}}
    """
    results = {}
    for t in tickers:
        score, headlines = get_ticker_news_sentiment(t)
        results[t] = {
            'score': score,
            'headlines': headlines
        }
    return results
