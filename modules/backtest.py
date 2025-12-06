import quantstats as qs
import pandas as pd
import numpy as np

# Silence matplotlib backend warnings if possible
# qs uses matplotlib inline usually, but for report generation it might try clear figures
# We can set backend to Agg to be safe for HTML generation
import matplotlib
matplotlib.use('Agg')

def run_full_backtest(weights, prices, benchmark_ticker="SPY"):
    """
    Runs a backtest using QuantStats.
    
    Args:
        weights (list): Portfolio weights.
        prices (pd.DataFrame): Historical Adjusted Close prices.
        benchmark_ticker (str): Ticker for benchmark.
        
    Returns:
        dict: Key metrics (Drawdown, Sortino, etc.)
        str: HTML report content
    """
    # 1. Calculate Portfolio Daily Returns
    returns = prices.pct_change(fill_method=None).dropna()
    
    # Portfolio Return Series = weighted sum of asset returns
    # weights must align with columns. prices columns are tickers.
    # Assuming weights list matches columns order of prices
    
    # Align weights to price columns just in case
    # (The app ensures weights match TICKERS list which matches prices columns)
    
    portfolio_returns = returns.dot(weights)
    portfolio_returns.name = "Portfolio"
    
    # 2. Get Benchmark
    # Check if we have SPY in prices already? Yes usually.
    if benchmark_ticker in prices.columns:
        benchmark_returns = returns[benchmark_ticker]
    else:
        # Fetch if missing (shouldn't happen with our default list)
        import yfinance as yf
        bench = yf.download(benchmark_ticker, period="5y", progress=False)['Adj Close']
        benchmark_returns = bench.pct_change(fill_method=None).dropna()
        
    # Align dates
    common_idx = portfolio_returns.index.intersection(benchmark_returns.index)
    portfolio_returns = portfolio_returns.loc[common_idx]
    benchmark_returns = benchmark_returns.loc[common_idx]
    
    # 3. Calculate Metrics
    metrics = {
        'max_drawdown': qs.stats.max_drawdown(portfolio_returns),
        'sortino': qs.stats.sortino(portfolio_returns),
        'sharpe': qs.stats.sharpe(portfolio_returns),
        'calmar': qs.stats.calmar(portfolio_returns),
        'win_rate': qs.stats.win_rate(portfolio_returns),
        'volatility': qs.stats.volatility(portfolio_returns)
    }
    
    # 4. Generate HTML Report
    # qs.reports.html returns the html string? No, it writes to file.
    # We need to capture it.
    output_file = "temp_qs_report.html"
    try:
        qs.reports.html(portfolio_returns, benchmark=benchmark_returns, output=output_file, title="FinAI Advanced Backtest", download_filename="finai_backtest.html")
        
        with open(output_file, "r", encoding='utf-8') as f:
            html_content = f.read()
            
    except Exception as e:
        print(f"QS Report Generation failed: {e}")
        html_content = "<html><body><h1>Error generating report</h1></body></html>"
        
    return metrics, html_content
