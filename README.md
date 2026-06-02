<div align="center">

# 🛍️ Rainshop POS

### Sistem Point of Sale dengan AI Image Search — Tanpa Barcode

*Kasir cukup arahkan barang ke kamera. Sistem mengenali sendiri.*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-2.x-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql)](https://mysql.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19-FF6F00?style=flat-square&logo=tensorflow)](https://tensorflow.org)
[![FAISS](https://img.shields.io/badge/FAISS-Meta_AI-0064E0?style=flat-square)](https://github.com/facebookresearch/faiss)
[![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-Live-222?style=flat-square&logo=github)](https://alaric2001.github.io/rainshop/)

**🔗 Live Demo: [alaric2001.github.io/rainshop](https://alaric2001.github.io/rainshop/)**

</div>

---

## ✨ Fitur Unggulan

### 🤖 AI Image Similarity Search
Tidak ada barcode? Tidak masalah. Sistem menggunakan **ResNet50** (ImageNet) untuk mengekstrak vektor fitur gambar 2048 dimensi, lalu **FAISS** (Facebook AI Similarity Search) untuk menemukan barang paling mirip dalam milidetik — teknologi yang sama digunakan Meta untuk pengenalan wajah di skala miliaran foto.

### 📱 Mobile-First & Responsive
Diakses dari PC kasir maupun smartphone dari jaringan mana saja. Tampilan otomatis menyesuaikan layar — tab switcher pada mobile, split-panel pada desktop.

### 🔒 HTTPS + Tunnel untuk Akses Kamera Mobile
Browser mobile memblokir akses kamera di HTTP. Rainshop menjalankan backend via **HTTPS** (self-signed cert untuk LAN, **ngrok** untuk akses internet) agar kamera HP bisa digunakan dari mana saja.

### 🖨️ Thermal Printer
Cetak struk langsung ke printer termal USB menggunakan **python-escpos** — format struk otomatis dengan nomor transaksi berurutan.

---

## 🏗️ Arsitektur

```
                    ┌─────────────────────────┐
                    │  GitHub Pages (Frontend) │
                    │  Vue.js 2 · BootstrapVue │
                    │  alaric2001.github.io    │
                    └────────────┬────────────┘
                                 │ HTTPS
                    ┌────────────▼────────────┐
                    │   ngrok Tunnel (HTTPS)   │
                    │  cube-judicial-amber...  │
                    └────────────┬────────────┘
                                 │
┌───────────────────┐  ┌─────────▼────────────────────────────┐
│  LAN (HTTPS:8080) │  │         Laptop / Server Lokal         │
│  webapp/ via      │  │  FastAPI · Uvicorn · port 8000        │
│  http-server      │  │  /items /images /sales /print-struk   │
└───────────────────┘  ├──────────────┬───────────────────────┤
                       │ SQLAlchemy   │ ResNet50 + FAISS       │
                       │ PyMySQL      │ python-escpos          │
                       └──────┬───────┴───────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │      MySQL 8.0      │
                    │  itembarang        │
                    │  item_images       │
                    │  sales_header      │
                    │  sales_line        │
                    └────────────────────┘
```

---

## 🧰 Tech Stack

| Layer | Teknologi |
|-------|-----------|
| **Backend** | FastAPI, SQLAlchemy 2, PyMySQL, Alembic |
| **AI / ML** | TensorFlow 2.19, ResNet50, FAISS-CPU |
| **Frontend** | Vue.js 2, BootstrapVue, Vuex, Vue Router |
| **Database** | MySQL 8, Stored Procedure, Views, Alembic Migrations |
| **Hardware** | Thermal printer USB (python-escpos, libusb) |
| **Deployment** | GitHub Pages, ngrok static tunnel, HTTPS self-signed |

---

## 🚀 Quick Start

### Prasyarat
- Python 3.11+
- Node.js 18+
- MySQL 8.0
- Git for Windows (menyertakan OpenSSL)

### 1 — Database

```sql
-- Jalankan satu file ini pada database kosong:
source db_script/rainshop_schema.sql
```

### 2 — Backend

```powershell
# Salin dan isi konfigurasi database
copy app\.env.example app\.env

# Install dependensi
pip install -r requirements.txt

# Generate SSL certificate (untuk akses kamera dari HP di LAN)
$ssl = "C:\Program Files\Git\usr\bin\openssl.exe"
& $ssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 825 -nodes `
  -subj "/CN=rainshop-local" `
  -addext "subjectAltName=IP:192.168.1.15,IP:127.0.0.1,DNS:localhost"
```

### 3 — Frontend

```powershell
cd client
npm install
npm run build        # build lokal → output ke ../webapp/
```

### 4 — Jalankan

```powershell
# Satu klik — membuka backend + frontend + ngrok sekaligus:
.\rainshop.bat
```

| Akses | URL |
|-------|-----|
| PC (lokal) | `https://127.0.0.1:8080` |
| HP (LAN) | `https://<IP-PC>:8080` |
| Internet (demo) | `https://alaric2001.github.io/rainshop/` |

> **Pertama kali akses dari HP via LAN:** buka `https://<IP-PC>:8000` lalu `https://<IP-PC>:8080`, ketuk *Advanced → Proceed* di keduanya.

---

## 🌐 Deploy ke GitHub Pages

Frontend di-host di GitHub Pages. Backend tetap di laptop, di-expose via **ngrok static domain** sehingga URL tidak berubah.

```powershell
# Setup ngrok (hanya sekali)
ngrok config add-authtoken <TOKEN_DARI_DASHBOARD_NGROK>

# Isi URL ngrok ke konfigurasi production
# Edit client/.env.production:
# VUE_APP_BASE_API=https://<ngrok-domain>.ngrok-free.dev

# Deploy frontend ke GitHub Pages
cd client
npm run deploy
```

---

## 📁 Struktur Repository

```
rainshop/
├── app/                       # Backend FastAPI
│   ├── models/                #   ORM models (SQLAlchemy)
│   ├── schemas/               #   Pydantic request/response
│   ├── crud/                  #   Database operations
│   ├── routers/               #   API endpoints
│   ├── utils/image_helper.py  #   ResNet50 + FAISS core
│   ├── .env                   #   Konfigurasi DB (tidak di-commit)
│   └── .env.example           #   Template konfigurasi DB
├── client/                    # Frontend Vue.js (source)
│   ├── src/
│   │   ├── views/             #   Halaman: POS, item-list, item-form, search
│   │   └── components/        #   CameraCapture (3 versi)
│   ├── .env.example           #   Template env development
│   └── .env.production.example #  Template env production (ngrok URL)
├── webapp/                    # Frontend build (served via http-server)
├── migrations/                # Alembic database migrations
├── db_script/
│   └── rainshop_schema.sql    # Schema lengkap — satu file, fresh install
├── rainshop.bat               # One-click launcher (backend + frontend + ngrok)
└── build-client.bat           # Build frontend → copy ke webapp/
```

---

## 🔄 Database Migration (Alembic)

```powershell
alembic current                                          # versi DB saat ini
alembic revision --autogenerate -m "tambah_kolom_xyz"   # buat migrasi baru
alembic upgrade head                                     # terapkan ke DB
alembic downgrade -1                                     # rollback satu versi
```

---

## 🤝 Kontak

Proyek ini dikembangkan untuk toko **Rain Shop** — toko pernak-pernik di Bojong Gede, Bogor.

📧 [alaric2001ra@gmail.com](mailto:alaric2001ra@gmail.com)  
🐙 [github.com/alaric2001](https://github.com/alaric2001)
