import streamlit as st

def display_methodology():
    st.title("Methodology & Academic Background 🎓")
    st.markdown("---")
    
    tab_en, tab_tr = st.tabs(["🇬🇧 English", "🇹🇷 Türkçe"])
    
    # --- English Content ---
    with tab_en:
        st.header("1. Modern Portfolio Theory (MPT)")
        st.write("""
        This Robo-Advisor utilizes **Harry Markowitz's Modern Portfolio Theory (1952)** to construct an Efficient Frontier. 
        The goal is to maximize returns for a given level of risk.
        """)
        
        st.subheader("Mathematical Model")
        st.write("**Portfolio Variance:**")
        st.latex(r"\sigma^2_p = \sum_{i} \sum_{j} w_i w_j \sigma_{ij}")
        st.write("Where $w_i, w_j$ are weights and $\sigma_{ij}$ is the covariance between assets $i$ and $j$.")
        
        st.write("**Sharpe Ratio Maximization:**")
        st.latex(r"S_p = \frac{R_p - R_f}{\sigma_p}")
        st.write("Where $R_p$ is portfolio return, $R_f$ is risk-free rate, and $\sigma_p$ is portfolio volatility.")
        
        st.divider()
        
        st.header("2. Monte Carlo Simulation")
        st.write("""
        To project future wealth, we use **Geometric Brownian Motion (GBM)**, a stochastic process that models stock prices.
        We run 1,000 parallel market scenarios over a 10-year horizon.
        """)
        st.latex(r"dS_t = \mu S_t dt + \sigma S_t dW_t")
        st.write("""
        - $\mu$: Drift (Expected Return)
        - $\sigma$: Volatility
        - $dW_t$: Wiener process (Random Shock)
        """)
        
        st.divider()
        
        st.header("3. AI Sentiment Analysis")
        st.write("""
        We integrate behavioral finance by adjusting portfolio weights based on news sentiment.
        - **Engine**: `TextBlob` (NLP Library)
        - **Process**: Fetches live news -> Calculates Polarity (-1 to +1) -> Modifies Optimization Constraints.
        """)
        
        st.divider()
        
        st.header("4. Risk Assessment Logic")
        st.write("""
        The "Risk Score" determining the user's profile is calculated based on:
        - **Age**: Younger investors get a higher risk capacity.
        - **Horizon**: Longer horizons allow for more aggressive strategies.
        - **Tolerance**: Subjective willingness to lose money.
        
        **Profiles:**
        - **Conservative**: Max 20% per asset. Focus on Bonds/Gold.
        - **Moderate**: Max 40% per asset. Balanced mix.
        - **Aggressive**: Max 70% per asset. High Equity/Crypto exposure.
        """)

    # --- Turkish Content ---
    with tab_tr:
        st.header("1. Modern Portföy Teorisi (MPT)")
        st.write("""
        Bu Robo-Danışman, Etkin Sınır (Efficient Frontier) oluşturmak için **Harry Markowitz'in Modern Portföy Teorisini** (1952) kullanır.
        Amaç, belirli bir risk seviyesi için getiriyi maksimize etmektir.
        """)
        
        st.subheader("Matematiksel Model")
        st.write("**Portföy Varyansı:**")
        st.latex(r"\sigma^2_p = \sum_{i} \sum_{j} w_i w_j \sigma_{ij}")
        st.write("Burada $w_i, w_j$ ağırlıkları, $\sigma_{ij}$ ise $i$ ve $j$ varlıkları arasındaki kovaryansı temsil eder.")
        
        st.write("**Sharpe Oranı Maksimizasyonu:**")
        st.latex(r"S_p = \frac{R_p - R_f}{\sigma_p}")
        st.write("$R_p$ portföy getirisi, $R_f$ risksiz faiz oranı ve $\sigma_p$ portföy oynaklığıdır.")
        
        st.divider()
        
        st.header("2. Monte Carlo Simülasyonu")
        st.write("""
        Gelecekteki varlık değerini tahmin etmek için hisse senedi fiyatlarını modelleyen stokastik bir süreç olan **Geometrik Brown Hareketi (GBM)** kullanılır.
        10 yıllık bir ufukta 1.000 paralel piyasa senaryosu çalıştırılır.
        """)
        st.latex(r"dS_t = \mu S_t dt + \sigma S_t dW_t")
        st.write("""
        - $\mu$: Drift (Beklenen Getiri)
        - $\sigma$: Volatilite (Oynaklık)
        - $dW_t$: Wiener süreci (Rastgele Şok)
        """)
        
        st.divider()
        
        st.header("3. Yapay Zeka (AI) Duygu Analizi")
        st.write("""
        Haber duyarlılığına dayalı olarak portföy ağırlıklarını ayarlayarak davranışsal finansı entegre ediyoruz.
        - **Motor**: `TextBlob` (Doğal Dil İşleme Kütüphanesi)
        - **Süreç**: Canlı haberleri çeker -> Polariteyi (-1 ila +1) hesaplar -> Optimizasyon kısıtlarını modifiye eder.
        """)
        
        st.divider()
        
        st.header("4. Risk Değerlendirme Mantığı")
        st.write("""
        Kullanıcının profilini belirleyen "Risk Skoru" şunlara dayanır:
        - **Yaş**: Genç yatırımcıların risk kapasitesi daha yüksektir.
        - **Vade**: Uzun vadeler daha agresif stratejilere izin verir.
        - **Tolerans**: Para kaybetme konusundaki öznel isteklilik.
        
        **Profiller:**
        - **Muhafazakar (Conservative)**: Varlık başına maks %20. Tahvil/Altın odaklı.
        - **Dengeli (Moderate)**: Varlık başına maks %40. Dengeli karışım.
        - **Agresif (Aggressive)**: Varlık başına maks %70. Yüksek Hisse/Kripto pozisyonu.
        """)
