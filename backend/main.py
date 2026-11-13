import re
from pathlib import Path
from urllib.parse import urlparse

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

bundle = joblib.load(Path(__file__).parent / "phishing_model.pkl")
model, FEATURES = bundle["model"], bundle["features"]


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


app = FastAPI(title="Phishing URL Detector")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class Req(BaseModel):
    url: str


@app.get("/")
def root():
    return {"status": "ok", "model_features": len(FEATURES)}


@app.post("/predict")
def predict(req: Req):
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL tidak boleh kosong")
    X = pd.DataFrame([extract(url)])[FEATURES]
    prob = float(model.predict_proba(X)[0][1])
    return {
        "url": url,
        "label": "phishing" if prob >= 0.5 else "legitimate",
        "probability_phishing": round(prob, 4),
    }
