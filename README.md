<div align="center">

# 🛡️ Deteksi URL Phishing

**Aplikasi web berbasis Machine Learning yang memprediksi apakah sebuah URL phishing atau aman, hanya dari pola teks URL-nya.**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-EC6B23)
![Streamlit](https://img.shields.io/badge/App-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![F1](https://img.shields.io/badge/F1--score-0.879-19B3A6)
![ROC-AUC](https://img.shields.io/badge/ROC--AUC-0.953-19B3A6)

[🚀 Coba Aplikasi](LINK_STREAMLIT_APP) · [📓 Notebook Google Colab](LINK_GOOGLE_COLAB) · [🎥 Video Presentasi](LINK_YOUTUBE)

</div>

---

## 📌 Tentang Proyek

Proyek ini adalah **Tugas Besar Machine Learning** yang dikerjakan dengan kerangka kerja **CRISP-DM**.

**Kebutuhan bisnis (ilustrasi):** sebuah bank digital ingin menyaring tautan phishing sebelum diklik nasabah, agar pencurian data dapat dicegah.

**Solusi:** model klasifikasi biner (*legitimate* atau *phishing*) yang dilatih dari fitur yang diekstrak langsung dari teks URL, lalu dibungkus menjadi aplikasi web sederhana.

## 📸 Tampilan Aplikasi

<!-- Taruh screenshot di folder screenshots/ lalu pastikan nama filenya sama -->
| URL aman | URL phishing |
|:---:|:---:|
| ![URL aman](screenshots/aman.png) | ![URL phishing](screenshots/phishing.png) |

## 🧠 Model dan Hasil

Dataset: [Web Page Phishing Detection Dataset](https://www.kaggle.com/datasets/shashwatwork/web-page-phishing-detection-dataset) (Kaggle), 11.429 URL setelah 1 duplikat dibuang, kelas seimbang (5.715 legitimate dan 5.714 phishing).

Tiga algoritma dibandingkan dengan `GridSearchCV` (5-fold, skor F1) pada data test 2.286 URL:

| Model | Train Acc | Test Acc | Precision | Recall | F1 | ROC-AUC | Kesimpulan fit |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| Logistic Regression | 0,8172 | 0,8136 | 0,8153 | 0,8110 | 0,8132 | 0,8994 | Underfit |
| Random Forest | 0,9779 | 0,8784 | 0,8791 | 0,8775 | 0,8783 | 0,9488 | Overfit |
| **XGBoost** | 0,9304 | 0,8797 | 0,8861 | 0,8714 | **0,8787** | **0,9526** | **Paling mendekati goodfit** |

**XGBoost** dipilih sebagai model akhir karena gap train dan test lebih kecil dari Random Forest dan ROC-AUC tertinggi.

> **Catatan:** dataset aslinya punya 86 fitur, sebagian bergantung data eksternal (misalnya `google_index` dan `page_rank`). Agar aplikasi bisa menerima URL yang diketik langsung, hanya **22 fitur dari teks URL** yang dipakai, seperti panjang URL, jumlah titik, tanda hubung, simbol `@`, rasio digit, jumlah subdomain, dan keberadaan alamat IP. Ini trade-off antara akurasi dan kelayakan implementasi.

## ⚙️ Alur Kerja

```
Dataset Kaggle → Google Colab (preprocessing, tuning, training) → xgb_model.json + scaler.json → Streamlit (app.py)
```

1. **Data preparation:** buang duplikat, ekstraksi 22 fitur, split 80:20 stratified, standardisasi (`StandardScaler`, fit hanya pada data train).
2. **Modeling:** Logistic Regression, Random Forest, XGBoost dengan tuning.
3. **Evaluation:** akurasi, precision, recall, F1, ROC-AUC, dan analisis goodfit.
4. **Deployment:** aplikasi Streamlit yang memuat model dari file JSON.

## 📁 Struktur Repository

```
.
├── app.py              # Antarmuka Streamlit + logika prediksi
├── xgb_model.json      # Model XGBoost hasil training di Colab
├── scaler.json         # Parameter StandardScaler dan daftar fitur
├── requirements.txt    # Dependensi Python
└── README.md
```

## 🚀 Cara Menjalankan di Komputer Sendiri

Butuh Python 3.10 atau lebih baru.

```bash
# 1. Clone repository
git clone https://github.com/USERNAME/NAMA_REPO.git
cd NAMA_REPO

# 2. Buat virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac / Linux

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py
```

Aplikasi terbuka di http://localhost:8501

## 🧪 Contoh URL untuk Dicoba

| URL | Perkiraan hasil |
|---|---|
| `https://www.google.com` | Aman |
| `http://192.168.1.1/secure-login-verify@bank-update.com/index.php?id=123` | Phishing |

## ⚠️ Keterbatasan

- Prediksi hanya berdasarkan **pola teks URL**, bukan isi halaman, usia domain, atau reputasi situs.
- Hasil **bukan jaminan keamanan 100%**. Tetap waspada terhadap tautan yang mencurigakan.
- Model dilatih pada satu dataset sehingga bisa kurang akurat pada pola phishing baru.

## 👤 Pembuat

**Izzan Khalish Zubair** · NPM 202343501347 · Kelas X7J
