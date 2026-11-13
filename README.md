# Deteksi URL Phishing (Tugas Besar Machine Learning - Part 3)

Nama: Izzan Khalish Zubair | NPM: 202343501347 | Kelas: X7J

Aplikasi web untuk memprediksi apakah sebuah URL phishing atau legitimate.
Model: XGBoost (dilatih di Google Colab, fitur diekstrak dari teks URL).

## Struktur
- `backend/` : FastAPI (`main.py`) + model `phishing_model.pkl`
- `frontend/` : antarmuka VueJS (`index.html`)

## Cara menjalankan
1. Backend
   ```
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
   API jalan di http://127.0.0.1:8000 (dokumentasi: /docs)
2. Frontend: buka `frontend/index.html` di browser.

## Endpoint
`POST /predict` dengan body `{"url": "http://contoh.com"}`
Respon: `{"url": "...", "label": "phishing|legitimate", "probability_phishing": 0.97}`
