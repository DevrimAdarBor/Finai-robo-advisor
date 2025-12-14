# FinAI - AI Destekli Robo Danışman 🤖📈

FinAI, yatırım stratejilerini analiz etmek, portföy performansını görselleştirmek ve veriye dayalı finansal içgörüler sunmak için tasarlanmış Python tabanlı bir robo-danışman projesidir.

Bu proje, finansal verileri işleyerek **QuantStats** kütüphanesi aracılığıyla detaylı performans raporları (Tear Sheets) oluşturur. 

## 🚀 Özellikler

* **Otomatik Veri Çekme:** Yahoo Finance API üzerinden güncel hisse senedi ve piyasa verilerini çeker.
* **Performans Analizi:** Kümülatif getiri, Sharpe oranı, maksimum düşüş (drawdown) gibi kritik metrikleri hesaplar.
* **Görsel Raporlama:** Strateji performansını S&P 500 (SPY) gibi kıyaslama ölçütleri (benchmark) ile karşılaştıran HTML formatında detaylı raporlar üretir.
* **Modüler Yapı:** Kolay geliştirilebilir ve ölçeklenebilir kod tabanı.

## 🛠️ Kullanılan Teknolojiler

* **Python 3.x**
* **yfinance:** Piyasa verilerini çekmek için.
* **QuantStats:** Finansal metrikleri hesaplamak ve raporlamak için.
* **Pandas & NumPy:** Veri manipülasyonu ve analizi için.

## 📂 Proje Yapısı

```bash
Finai-robo-advisor/
├── app.py                # Uygulamanın ana giriş noktası
├── modules/              # Yardımcı fonksiyonlar ve analiz modülleri
├── utils/                # Araçlar ve konfigürasyon dosyaları
├── temp_qs_report.html   # Örnek oluşturulmuş performans raporu
└── requirements.txt      # Gerekli kütüphaneler
