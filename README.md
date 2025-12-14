# 📈 FinAI: Intelligent Robo-Advisor & Portfolio Optimizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://finai-robo-advisor-pj5iql9jubzinbn4cnqt2w.streamlit.app/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FinAI** is a comprehensive, AI-powered financial dashboard designed to democratize professional-grade portfolio management. It combines **Modern Portfolio Theory (MPT)** with **Monte Carlo simulations** and **Real-Time Market Data** to provide users with data-driven investment strategies.

🚀 **Live Demo:** [Click here to launch the app](https://finai-robo-advisor-pj5iql9jubzinbn4cnqt2w.streamlit.app/)

---

## 🌟 Key Features

### 1. 🧠 Smart Asset Allocation
- Utilizes **Markowitz Mean-Variance Optimization** to construct efficient portfolios.
- Dynamically adjusts asset weights (Equities, Bonds, Gold, Crypto) based on the user's risk profile (Conservative to Aggressive).
- Calculates **Sharpe Ratio**, Volatility, and Expected Returns in real-time.

### 2. 🎲 Monte Carlo Simulation
- Projects future portfolio performance using **Geometric Brownian Motion (GBM)**.
- Simulates **1,000+ market scenarios** to visualize potential outcomes over a 10-year horizon.
- Provides Confidence Intervals (95%) for risk assessment.

### 3. 📰 Real-Time Market Intelligence
- **Live News Ticker:** Integrates RSS feeds from major financial news outlets (Yahoo Finance, Bloomberg logic) to display scrolling breaking news.
- **Sentiment Analysis:** (Beta) Analyzes market sentiment to provide context for volatility.

### 4. 📊 Institutional-Grade Reporting
- Generates downloadable **PDF Reports** via `QuantStats`.
- Includes max drawdown analysis, win/loss ratios, and monthly return heatmaps.

---

## 🛠️ Tech Stack & Methodology

This project is built using Python and leverages key libraries for quantitative finance:

* **Core Framework:** `Streamlit` (Web UI)
* **Data Engine:** `yfinance` (Market Data), `feedparser` (RSS News)
* **Quantitative Analysis:** `NumPy`, `Pandas`, `SciPy` (Optimization)
* **Visualization:** `Plotly` (Interactive Charts), `Matplotlib`
* **Financial Metrics:** `QuantStats`

### Mathematical Model
The core optimization solves for the weights $w$ that maximize the Sharpe Ratio:

$$
\text{Maximize } S_p = \frac{R_p - R_f}{\sigma_p}
$$

Where:
* $R_p$: Expected Portfolio Return
* $R_f$: Risk-Free Rate
* $S_p$: Portfolio Standard Deviation

---

## 📂 Project Structure

```text
├── app.py                 # Main application entry point
├── modules/
│   ├── data_engine.py     # Fetches stock prices and RSS news
│   ├── monte_carlo.py     # Stochastic simulation logic
│   ├── portfolio.py       # MPT optimization algorithms
│   ├── ui_components.py   # Charts, Tickers, and UI styling
│   └── utils.py           # Helper functions (PDF generation)
├── assets/                # Images and static files
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

## 👨‍💻 Author

Developed by Devrim Adar Bor
* Management Information Systems Student at Dokuz Eylul University
* Aspiring Financial Engineer
