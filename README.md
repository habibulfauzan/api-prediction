---
title: Diabetes Prediction API
emoji: 🩺
colorFrom: blue
colorTo: green
sdk: docker
---

# API Prediksi Diabetes (Flask)

Backend API untuk prediksi diabetes menggunakan model Random Forest.

## Deploy ke Hugging Face Spaces (Docker)

Karena backend ini **Flask API** (bukan Gradio), cara deploy yang paling cocok di Hugging Face adalah **Space jenis Docker**.

### 1) Buat Space

- **New Space** di Hugging Face
- **Space SDK**: pilih **Docker**
- **Visibility**: sesuai kebutuhan (Public/Private)

### 2) Struktur file minimal

Pastikan folder `backend/` berisi minimal:

- **`app.py`**: Flask app (harus mengekspor variabel `app`)
- **`rf_inference.pkl`**: model pipeline yang dipakai inference (dibaca oleh `app.py`)
- **`requirements.txt`**: dependensi Python untuk inference + server
- **`Dockerfile`**: untuk menjalankan API di Spaces

Catatan: di `app.py` saat ini model dibaca lewat path relatif:
`with open('rf_inference.pkl', 'rb') ...` jadi file `rf_inference.pkl` harus berada di **root Space** (atau sesuaikan path).

### 3) Contoh `Dockerfile` (recommended)

Buat `backend/Dockerfile` seperti ini (atau taruh di root repo dan sesuaikan `COPY`):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 7860

# Hugging Face Spaces mengharapkan service listen di 7860
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app", "--workers", "1", "--threads", "4", "--timeout", "120"]
```

### 4) Contoh `requirements.txt`

Minimal yang umum dipakai untuk project ini:

```txt
flask
flask-cors
gunicorn
numpy
pandas
scikit-learn
```

Jika model pipeline kamu memakai library lain (mis. `xgboost`, `imblearn`, `category_encoders`, dll), tambahkan juga.

### 5) Upload ke Space

Opsi termudah:

- Upload semua file `backend/` ke root repository Space, atau
- Hubungkan Space ke GitHub repo kamu dan pastikan `Dockerfile` + `requirements.txt` ada di lokasi yang dibaca build.

Jika kamu taruh backend di subfolder, pastikan `Dockerfile` menyesuaikan `COPY` dan `WORKDIR` (atau gunakan “Repository directory” di pengaturan Space).

### 6) Endpoint yang tersedia

- **GET `/`**: health check
- **POST `/predict`**: prediksi

Contoh request:

```bash
curl -X POST "https://<username>-<space>.hf.space/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"gender\":\"Female\",\"age\":45,\"hypertension\":0,\"heart_disease\":0,\"smoking_history\":\"never\",\"bmi\":27.5,\"HbA1c_level\":5.9,\"blood_glucose_level\":120}"
```

### 7) Troubleshooting cepat

- **Build sukses tapi 500 saat predict**: biasanya `rf_inference.pkl` tidak ikut ter-upload / path salah.
- **Import error**: tambah library yang kurang ke `requirements.txt`.
- **CORS**: sudah diizinkan `*` via `flask_cors` (lihat `app.py`).
