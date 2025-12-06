import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def plot_portfolio_allocation(weights, tickers):
    """
    Creates a pie chart for portfolio allocation.
    """
    # Filter out zero weights
    labels = []
    values = []
    for t, w in zip(tickers, weights):
        if w > 0.01:
            labels.append(t)
            values.append(w)
            
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text="Recommended Portfolio Allocation")
    return fig

def plot_efficient_frontier(frontier_data, risk_free_rate=0.0):
    """
    Plots the efficient frontier (if we had full curve data)
    For now, we just plot the optimal points.
    Future improvement: Generate random portfolios to show the curve.
    """
    # Generate random portfolios to show the cloud
    # (Simplified for this function, assuming we pass the specific points only)
    
    # We will create a simple scatter of the two main points + User Choice
    
    sharpe = frontier_data['Max Sharpe']
    min_vol = frontier_data['Min Volatility']
    
    fig = go.Figure()
    
    # Max Sharpe
    fig.add_trace(go.Scatter(
        x=[sharpe['volatility']], y=[sharpe['return']],
        mode='markers+text',
        marker=dict(symbol='star', size=15, color='red'),
        text=['Max Sharpe'], textposition="top center",
        name='Max Sharpe'
    ))
    
    # Min Vol
    fig.add_trace(go.Scatter(
        x=[min_vol['volatility']], y=[min_vol['return']],
        mode='markers+text',
        marker=dict(symbol='triangle-up', size=15, color='blue'),
        text=['Min Volatility'], textposition="top center",
        name='Min Volatility'
    ))
    
    fig.update_layout(
        title='Optimal Portfolios',
        xaxis_title='Volatility (Std. Dev)',
        yaxis_title='Expected Annual Return',
        showlegend=True
    )
    return fig

def plot_performance_comparison(portfolio_cum_return, benchmark_cum_return, benchmark_name="S&P 500"):
    """
    Plots a line chart comparing portfolio vs benchmark.
    Args:
        portfolio_cum_return (pd.Series): Cumulative returns of the portfolio.
        benchmark_cum_return (pd.Series): Cumulative returns of the benchmark.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=portfolio_cum_return.index, 
        y=portfolio_cum_return.values, 
        mode='lines', 
        name='Your Portfolio'
    ))
    
    fig.add_trace(go.Scatter(
        x=benchmark_cum_return.index, 
        y=benchmark_cum_return.values, 
        mode='lines', 
        name=benchmark_name,
        line=dict(dash='dash')
    ))
    
    fig.update_layout(title='Portfolio vs Benchmark Performance (Historical Simulation)',
                      yaxis_title='Cumulative Return', xaxis_title='Date')
    return fig

def plot_monte_carlo(simulation_results, summary):
    """
    Plots the cone chart for Monte Carlo simulation.
    """
    fig = go.Figure()
    
    # Reset index to use as x-axis (Trading Days)
    # Downsample for plotting performance if too large
    df = simulation_results
    if len(df) > 1000:
        step = len(df) // 500
        df = df.iloc[::step]
    
    # Plot top 100 paths roughly to show spread
    subset = df.iloc[:, :50] 
    for col in subset.columns:
        fig.add_trace(go.Scatter(
            x=subset.index, y=subset[col],
            mode='lines',
            line=dict(color='rgba(100, 100, 100, 0.1)', width=1),
            showlegend=False,
            hoverinfo='skip'
        ))
        
    # Plot Percentiles
    # We need to calculate percentiles over time for the cone
    # Re-calculate full percentiles for plotting
    quantiles = simulation_results.quantile([0.05, 0.5, 0.95], axis=1).T
    if len(quantiles) > 1000:
        step = len(quantiles) // 500
        quantiles = quantiles.iloc[::step]

    fig.add_trace(go.Scatter(
        x=quantiles.index, y=quantiles[0.95],
        mode='lines', name='95th Percentile',
        line=dict(color='green', dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=quantiles.index, y=quantiles[0.5],
        mode='lines', name='Median',
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatter(
        x=quantiles.index, y=quantiles[0.05],
        mode='lines', name='5th Percentile',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(
        title='Monte Carlo Simulation (10 Year Projection)',
        yaxis_title='Portfolio Value ($)',
        xaxis_title='Trading Days',
        template='plotly_dark'
    )
    return fig

def plot_candlestick(data, ticker):
    """
    Plots a candlestick chart for a single asset.
    """
    if data.empty:
        return go.Figure()
        
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])

    fig.update_layout(
        title=f'{ticker} Price History',
        yaxis_title='Price',
        template='plotly_dark'
    )
    return fig
