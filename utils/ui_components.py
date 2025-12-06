import streamlit as st

def display_news_ticker(news_list):
    """
    Displays a scrolling news ticker at the bottom of the screen.
    """
    news_text = "   +++   ".join(news_list) + "   +++   "
    
    # CSS for the ticker
    ticker_css = f"""
    <style>
    .ticker-wrap {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        overflow: hidden;
        background-color: #1e1e1e;
        color: #00ff41; /* Terminal Green */
        font-family: 'Courier New', monospace;
        font-size: 16px;
        line-height: 40px;
        white-space: nowrap;
        z-index: 9999;
        border-top: 2px solid #333;
    }}
    
    .ticker {{
        display: inline-block;
        padding-left: 100%;
        animation: ticker 45s linear infinite;
    }}
    
    @keyframes ticker {{
        0% {{ transform: translate3d(0, 0, 0); }}
        100% {{ transform: translate3d(-100%, 0, 0); }}
    }}
    </style>
    
    <div class="ticker-wrap">
        <div class="ticker">{news_text}</div>
    </div>
    """
    
    st.markdown(ticker_css, unsafe_allow_html=True)
