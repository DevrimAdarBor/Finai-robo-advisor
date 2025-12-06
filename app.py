import streamlit as st
import pandas as pd
import numpy as np
import time
from streamlit_option_menu import option_menu

# Import modules
try:
    from modules import risk_assessment, data_engine, optimization, sentiment, simulation, reporting, backtest, methodology
    from utils import visualizations, ui_components
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# --- Config & Styling ---
st.set_page_config(page_title="FinAI Robo-Advisor", layout="wide", page_icon="📈")

# Custom CSS for "Dark Mode Fintech" look
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Metrics Cards */
    div.css-1r6slb0.e1tzin5v2 {
        background-color: #1E1E1E;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #00ADB5;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #00FFF5;
        color: black;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #222831;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #EEEEEE;
    }
    
    /* Metric Value */
    [data-testid="stMetricValue"] {
        color: #00ADB5 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Constants ---
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'SPY', 'GLD', 'BTC-USD']

# --- Sidebar Navigation ---
with st.sidebar:
    st.warning("⚠️ EDUCATIONAL PURPOSE ONLY.\n\nThis application is a university project. It is NOT financial advice. Do not use for real trading.")
    selected = option_menu(
        "FinAI Advisor", 
        ["Home", "Asset Analysis", "Monte Carlo Sim", "Advanced Backtest", "Methodology"], 
        icons=['house', 'graph-up', 'cpu', 'clipboard-data', 'book'], 
        menu_icon="robot", 
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#222831"},
            "icon": {"color": "#00ADB5", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#393E46"},
            "nav-link-selected": {"background-color": "#393E46"},
        }
    )
    
    st.markdown("---")
    st.header("Risk Profile")
    age = st.number_input("Age", 18, 100, 30)
    horizon = st.selectbox("Horizon", ('Short (0-3y)', 'Medium (3-7y)', 'Long (7y+)'))
    tolerance = st.selectbox("Tolerance", ('Low', 'Moderate', 'High'))
    knowledge = st.selectbox("Knowledge", ('None', 'Some', 'Extensive'))
    
    if st.button("Update Profile"):
        risk_profile = risk_assessment.calculate_risk_profile(age, horizon, tolerance, knowledge)
        st.session_state['risk_profile'] = risk_profile
        st.rerun()

                
# --- State Management ---
if 'risk_profile' not in st.session_state:
    st.session_state['risk_profile'] = risk_assessment.calculate_risk_profile(age, horizon, tolerance, knowledge)

# Load Data (Cached if possible in real app, here we just load once per session or reload)
if 'prices' not in st.session_state:
    with st.spinner("Initializing Market Data Engine..."):
        st.session_state['prices'] = data_engine.get_historical_data(TICKERS, period="2y")
        st.session_state['sentiment'] = sentiment.get_market_sentiment(TICKERS)

rp = st.session_state['risk_profile']
prices = st.session_state['prices']
sentiments = st.session_state['sentiment']

# --- Helper Logic ---
def get_optimized_portfolio():
    if prices.empty:
        return None, None, None
        
    returns = prices.pct_change(fill_method=None).dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    # --- Logic Fix: Diversification Constraints ---
    # Conservative: Max 20% per asset (forces >=5 assets)
    # Moderate: Max 40% per asset
    # Aggressive: Max 70% per asset
    
    max_weight = 1.0
    if rp['risk_level'] == "Conservative":
        max_weight = 0.20
    elif rp['risk_level'] == "Moderate":
        max_weight = 0.40
    elif rp['risk_level'] == "Aggressive":
        max_weight = 0.70
        
    frontier = optimization.get_efficient_frontier(mean_returns, cov_matrix, len(TICKERS), asset_max_weight=max_weight)
    
    if rp['risk_level'] == "Aggressive":
        optimal = frontier['Max Sharpe']
    else:
        optimal = frontier['Min Volatility']
        
    # AI Adjustment
    flat_weights = list(optimal['weights'])
    for i, t in enumerate(TICKERS):
        s = sentiments.get(t, {'score': 0})
        if s['score'] > 0.1: flat_weights[i] *= 1.1
        elif s['score'] < -0.1: flat_weights[i] *= 0.9
    
    total = sum(flat_weights)
    final_weights = [w/total for w in flat_weights]
    
    return final_weights, mean_returns, cov_matrix

# --- Sidebar Report Button (Placed here to access data) ---
with st.sidebar:
    if 'prices' in st.session_state and not st.session_state['prices'].empty:
        st.markdown("---")
        st.header("Downloads")
        
        # Calculate now for the report
        r_weights, r_mean_rets, r_cov_mat = get_optimized_portfolio()
        
        if r_weights:
            r_ret, r_vol = optimization.portfolio_annualised_performance(np.array(r_weights), r_mean_rets, r_cov_mat)
            r_metrics = {
                'return': r_ret,
                'volatility': r_vol,
                'sharpe': (r_ret - 0.02) / r_vol
            }
            
            # Check for simulation results in session (optional)
            sim_summary = st.session_state.get('sim_summary', None)
            
            pdf_data = reporting.generate_report(rp, r_weights, TICKERS, r_metrics, sim_summary)
            
            st.download_button(
                label="📄 Download Investment Report",
                data=pdf_data,
                file_name="FinAI_Report.pdf",
                mime="application/pdf"
            )

# --- Pages ---

if selected == "Home":
    st.title(f"Welcome, Investor! 🚀")
    
    # 1. Top Metric Cards
    weights, mean_rets, cov_mat = get_optimized_portfolio()
    
    if weights:
        ret, vol = optimization.portfolio_annualised_performance(np.array(weights), mean_rets, cov_mat)
        sharpe = (ret - 0.02) / vol
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Risk Score", rp['score'], rp['risk_level'])
        col2.metric("Exp. Return", f"{ret:.1%}", "Annual")
        col3.metric("Volatility", f"{vol:.1%}", "Risk")
        col4.metric("Sharpe Ratio", f"{sharpe:.2f}", "Efficiency")
        
        st.markdown("---")
        
        # 2. Main Dashboard
        col_pie, col_frontier = st.columns([1, 1])
        
        with col_pie:
            st.subheader("Asset Allocation")
            fig = visualizations.plot_portfolio_allocation(weights, TICKERS)
            st.plotly_chart(fig, use_container_width=True)
            
        with col_frontier:
            st.subheader("Efficient Frontier")
            # We need to re-calc frontier for the plot
            returns = prices.pct_change(fill_method=None).dropna()
            frontier = optimization.get_efficient_frontier(returns.mean(), returns.cov(), len(TICKERS))
            fig = visualizations.plot_efficient_frontier(frontier)
            st.plotly_chart(fig, use_container_width=True)
            
        st.info(f"**AI Insight**: Based on your {rp['risk_level']} profile and current market sentiment, we adjusted weights for positive sentiment assets.")

    # --- About & Disclaimer ---
    st.markdown("---")
    with st.expander("ℹ️ About this Project"):
        st.write("""
        This app is a **Senior Capstone Project** for the **Dokuz Eylul University MIS Department**.
        It utilizes Python, Modern Portfolio Theory, and AI-driven sentiment analysis to simulate a Robo-Advisor experience.
        """)
        
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8em; margin_top: 20px;'>
        Disclaimer: The content provided by FinAI is for informational purposes only. The developer is not a registered financial advisor. Investment involves risk.
    </div>
    """, unsafe_allow_html=True)

elif selected == "Asset Analysis":
    st.title("Deep Dive Asset Analysis 🔍")
    
    target_asset = st.selectbox("Select Asset", TICKERS)
    
    col_chart, col_info = st.columns([3, 1])
    
    with col_chart:
        data = data_engine.get_ohlc_data(target_asset, period="1y")
        
        if not data.empty:
            fig = visualizations.plot_candlestick(data, target_asset)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Market data not available for {target_asset}. Please check your internet connection or the ticker symbol.")
        
    with col_info:
        st.subheader("Sentiment")
        s = sentiments.get(target_asset, {'score': 0, 'headlines': []})
        st.metric("Sentiment Score", f"{s['score']:.2f}")
        
        st.markdown("**Recent Headlines:**")
        for h in s['headlines'][:3]:
            st.markdown(f"- *{h}*")

elif selected == "Monte Carlo Sim":
    st.title("Future Wealth Projection 🔮")
    
    st.markdown("Run a Monte Carlo simulation to estimate the range of portfolio outcomes over the next 10 years.")
    
    init_inv = st.number_input("Initial Investment ($)", 1000, 1000000, 10000)
    
    if st.button("Run Simulation"):
        weights, mean_rets, cov_mat = get_optimized_portfolio()
        
        with st.spinner("Simulating 1000 market scenarios..."):
            sim_results, summary = simulation.run_monte_carlo(weights, mean_rets, cov_mat, years=10, initial_portfolio=init_inv)
            st.session_state['sim_summary'] = summary
            
        # Metrics
        st.success("Simulation Complete!")
        m1, m2, m3 = st.columns(3)
        m1.metric("Optimistic (95th)", f"${summary['95th Percentile']:,.0f}")
        m2.metric("Median (50th)", f"${summary['50th Percentile']:,.0f}")
        m3.metric("Pessimistic (5th)", f"${summary['5th Percentile']:,.0f}")
        
        # Chart
        fig = visualizations.plot_monte_carlo(sim_results, summary)
        st.plotly_chart(fig, use_container_width=True)

elif selected == "Advanced Backtest":
    st.title("Advanced Quantitative Backtest 📊")
    st.markdown("Powered by **QuantStats**")
    
    weights, mean_rets, cov_mat = get_optimized_portfolio()
    
    if weights:
        if st.button("Run Full Backtest"):
            with st.spinner("Crunching numbers... this may take a moment"):
                # Run Backtest
                metrics, html_report = backtest.run_full_backtest(weights, prices, benchmark_ticker="SPY")
                
                # Metrics Grid
                st.subheader("Key Performance Metrics")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Max Drawdown", f"{metrics['max_drawdown']:.2%}")
                c2.metric("Sortino Ratio", f"{metrics['sortino']:.2f}")
                c3.metric("Calmar Ratio", f"{metrics['calmar']:.2f}")
                c4.metric("Win Rate", f"{metrics['win_rate']:.2%}")
                
                st.markdown("---")
                
                # HTML Download
                st.subheader("Full Professional Tearsheet")
                st.info("Download the full HTML report for deep-dive analytics (Rolling Volatility, EoY Returns, Monthly Heatmaps, etc.)")
                
                st.download_button(
                    label="📥 Download QuantStats Report (HTML)",
                    data=html_report,
                    file_name="FinAI_QuantStats_Report.html",
                    mime="text/html"
                )
    else:
        st.warning("Please setup your portfolio first on the Home page.")

elif selected == "Methodology":
    methodology.display_methodology()
    
# --- Global Elements ---
# News Ticker (Bloomberg Style)
if 'news_ticker' not in st.session_state:
    try:
        st.session_state['news_ticker'] = data_engine.get_general_market_news()
    except:
        st.session_state['news_ticker'] = ["Market Data Unavailable"]

ui_components.display_news_ticker(st.session_state['news_ticker'])
