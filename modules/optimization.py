import numpy as np
import scipy.optimize as sco

def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    """
    Calculates portfolio performance (return, volatility).
    Assumes 252 trading days.
    """
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return returns, std

def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    p_ret, p_var = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_var

def get_efficient_frontier(mean_returns, cov_matrix, num_assets, risk_free_rate=0.0, asset_max_weight=1.0):
    """
    Calculates the efficient frontier and optimal weights.
    
    Args:
        mean_returns (pd.Series): Average daily returns.
        cov_matrix (pd.DataFrame): Covariance matrix of returns.
        num_assets (int): Number of assets.
        risk_free_rate (float): Risk-free rate approximation (e.g. 0.02).
        asset_max_weight (float): Maximum weight allowed for a single asset (0.0 to 1.0).
        
    Returns:
        dict: {
            'Max Sharpe': {'weights': [], 'return': float, 'volatility': float},
            'Min Volatility': {'weights': [], 'return': float, 'volatility': float}
        }
    """
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, asset_max_weight) for asset in range(num_assets))
    
    # 1. Maximize Sharpe Ratio
    result_sharpe = sco.minimize(neg_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                                 method='SLSQP', bounds=bounds, constraints=constraints)
    
    # 2. Minimize Volatility
    def get_volatility(weights, mean_returns, cov_matrix):
        return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[1]
        
    result_min_vol = sco.minimize(get_volatility, num_assets*[1./num_assets,], args=(mean_returns, cov_matrix),
                                  method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Get details
    sharpe_ret, sharpe_vol = portfolio_annualised_performance(result_sharpe.x, mean_returns, cov_matrix)
    min_vol_ret, min_vol_vol = portfolio_annualised_performance(result_min_vol.x, mean_returns, cov_matrix)
    
    return {
        'Max Sharpe': {
            'weights': result_sharpe.x,
            'return': sharpe_ret,
            'volatility': sharpe_vol,
            'sharpe': (sharpe_ret - risk_free_rate) / sharpe_vol
        },
        'Min Volatility': {
            'weights': result_min_vol.x,
            'return': min_vol_ret,
            'volatility': min_vol_vol,
            'sharpe': (min_vol_ret - risk_free_rate) / min_vol_vol
        }
    }
