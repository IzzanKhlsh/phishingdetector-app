import json
import re
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import streamlit as st
import xgboost as xgb

DIR = Path(__file__).parent


@st.cache_resource
def load_model():
    meta = json.load(open(DIR / "scaler.json"))
    booster = xgb.Booster()
    booster.load_model(str(DIR / "xgb_model.json"))
    return booster, meta["features"], np.array(meta["mean"]), np.array(meta["scale"])


def extract(url):
    # Harus sama persis dengan fungsi extract() di notebook Colab
    u = url.strip()
    p = urlparse(u if '://' in u else 'http://' + u)
    h = p.hostname or ''
    L = u.lower()
    return {
        'length_url': len(u), 'length_hostname': len(h),
        'ip': int(bool(re.fullmatch(r'[\d.]+', h))),
        'nb_dots': u.count('.'), 'nb_hyphens': u.count('-'), 'nb_at': u.count('@'),
        'nb_qm': u.count('?'), 'nb_and': u.count('&'), 'nb_eq': u.count('='),
        'nb_underscore': u.count('_'), 'nb_percent': u.count('%'),
        'nb_slash': u.count('/'), 'nb_colon': u.count(':'),
        'nb_www': L.count('www'), 'nb_com': L.count('.com'),
        'nb_dslash': int(u.rfind('//') > 7),
        'http_in_path': int('http' in (p.path + p.query).lower()),
        'https_token': int('https' in h.lower()),
        'ratio_digits_url': sum(c.isdigit() for c in u) / max(len(u), 1),
        'ratio_digits_host': sum(c.isdigit() for c in h) / max(len(h), 1),
        'nb_subdomains': max(len(h.split('.')) - 2, 0),
        'prefix_suffix': int('-' in h),
    }


st.set_page_config(page_title="Deteksi URL Phishing", page_icon="🛡️")
st.title("🛡️ Deteksi URL Phishing")
st.caption("Model XGBoost yang memprediksi apakah sebuah URL phishing atau aman.")

booster, FEATURES, MEAN, SCALE = load_model()

url = st.text_input("Masukkan URL", placeholder="http://login-bank.example.com/verify?id=1")

if st.button("Periksa URL", type="primary"):
    if not url.strip():
        st.warning("URL tidak boleh kosong.")
    else:
        feats = extract(url)
        X = (pd.DataFrame([feats])[FEATURES].values - MEAN) / SCALE
        prob = float(booster.predict(xgb.DMatrix(X))[0])
        if prob >= 0.5:
            st.error(f"PHISHING (probabilitas {prob * 100:.1f}%)")
        else:
            st.success(f"AMAN / Legitimate (probabilitas phishing {prob * 100:.1f}%)")
        st.progress(min(max(prob, 0.0), 1.0))
        with st.expander("Lihat fitur yang diekstrak dari URL"):
            st.dataframe(pd.DataFrame([feats]).T.rename(columns={0: "nilai"}))

st.caption("Prediksi hanya berdasarkan pola teks URL, bukan jaminan keamanan 100%.")
