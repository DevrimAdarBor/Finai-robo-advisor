import numpy as np
import pandas as pd

def run_monte_carlo(weights, mean_returns, cov_matrix, years=10, simulations=1000, initial_portfolio=10000):
    """
    Runs a Monte Carlo simulation for portfolio growth.
    
    Args:
        weights (list): Portfolio weights.
        mean_returns (pd.Series): Mean daily returns.
        cov_matrix (pd.DataFrame): Covariance matrix.
        years (int): Number of years to simulate.
        simulations (int): Number of simulation runs.
        initial_portfolio (float): Initial investment amount.
        
    Returns:
        pd.DataFrame: DataFrame of all simulation paths (rows=days, cols=simulations).
        dict: Summary statistics (5th, 50th, 95th percentiles of final value).
    """
    weights = np.array(weights)
    mean_return = np.sum(mean_returns * weights)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    days = years * 252
    
    # Generate random Z-scores
    # Shape: (days, simulations)
    Z = np.random.normal(size=(days, simulations))
    
    # Calculate daily returns: mu/252 + sigma/sqrt(252) * Z
    # Note: Using geometric Brownian motion approximation
    # daily_ret = mean_return + portfolio_std * Z 
    # But usually we sim log returns or just simple daily returns. 
    # Let's use simple daily returns for this estimation.
    
    daily_returns = mean_return + portfolio_std * Z
    
    # Accumulate returns
    price_paths = np.zeros_like(daily_returns)
    price_paths[0] = initial_portfolio
    
    for t in range(1, days):
        price_paths[t] = price_paths[t-1] * (1 + daily_returns[t])
        
    results_df = pd.DataFrame(price_paths)
    
    # Calculate percentiles
    final_values = results_df.iloc[-1]
    p05 = np.percentile(final_values, 5)
    p50 = np.percentile(final_values, 50)
    p95 = np.percentile(final_values, 95)
    
    summary = {
        "5th Percentile": p05,
        "50th Percentile": p50,
        "95th Percentile": p95
    }
    
    return results_df, summary
