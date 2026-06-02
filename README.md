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

</div>

---

## ✨ Fitur Unggulan

### 🤖 AI Image Similarity Search
Tidak ada barcode? Tidak masalah. Sistem menggunakan **ResNet50** (ImageNet) untuk mengekstrak vektor fitur gambar 2048 dimensi, lalu **FAISS** (Facebook AI Similarity Search) untuk menemukan barang paling mirip dalam milidetik — teknologi yang sama digunakan Meta untuk pengenalan wajah di skala miliaran foto.

### 📱 Mobile-First & Responsive
Diakses dari PC kasir maupun smartphone kasir lain di jaringan yang sama. Tampilan otomatis menyesuaikan layar — tab switcher pada mobile, split-panel pada desktop.

### 🔒 HTTPS untuk Akses Kamera Mobile
Browser mobile memblokir akses kamera di HTTP. Rainshop menjalankan frontend dan backend via **HTTPS** (self-signed cert) agar kamera HP bisa digunakan dari jaringan LAN.

### 🖨️ Thermal Printer
Cetak struk langsung ke printer termal USB menggunakan **python-escpos** — format struk otomatis dengan nomor transaksi berurutan.

---

## 🏗️ Arsitektur

```
┌─────────────────────────────────────────────────────────┐
│                    Browser / HP Kasir                   │
│              Vue.js 2  ·  BootstrapVue  ·  Axios        │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS :8080
┌──────────────────────▼──────────────────────────────────┐
│               webapp/  (static build)                   │
│                    http-server                          │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS :8000
┌──────────────────────▼──────────────────────────────────┐
│              FastAPI  (Python 3.11)                     │
│   /items  /images  /sales  /print-struk  /voiceover     │
├─────────────────┬────────────────────────────────────── ┤
│   SQLAlchemy    │   ResNet50 + FAISS (image search)     │
│   PyMySQL       │   python-escpos (thermal printer)     │
└────────┬────────┴────────────────────────────────────── ┘
         │
┌────────▼────────┐
│   MySQL 8.0     │
│  itembarang     │
│  item_images    │
│  sales_header   │
│  sales_line     │
└─────────────────┘
```

---

## 🧰 Tech Stack

| Layer | Teknologi |
|-------|-----------|
| **Backend** | FastAPI, SQLAlchemy 2, PyMySQL, Alembic |
| **AI / ML** | TensorFlow 2.19, ResNet50, FAISS-CPU |
| **Frontend** | Vue.js 2, BootstrapVue, Vuex, Vue Router |
| **Database** | MySQL 8, stored procedure, views |
| **Hardware** | Thermal printer USB (python-escpos, libusb) |
| **Infra** | HTTPS (self-signed), http-server, Uvicorn |

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
# Konfigurasi database
copy app\.env.example app\.env   # lalu isi DB_PASSWORD

# Install dependensi
pip install -r requirements.txt

# Generate SSL certificate (untuk akses kamera dari HP)
$ssl = "C:\Program Files\Git\usr\bin\openssl.exe"
& $ssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 825 -nodes `
  -subj "/CN=rainshop-local" `
  -addext "subjectAltName=IP:$(
    (Get-NetIPAddress -AddressFamily IPv4 | Where IPAddress -match '^192\.' | Select -First 1).IPAddress
  ),IP:127.0.0.1,DNS:localhost"
```

### 3 — Frontend

```powershell
cd client
npm install
npm run build        # output → ../webapp/
```

### 4 — Jalankan

```powershell
# Semua sekaligus (backend + frontend + buka browser):
.\rainshop.bat

# Atau manual:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile key.pem --ssl-certfile cert.pem --reload
```

> **Akses dari HP:** Buka `https://<IP-PC>:8080` → ketuk *Advanced → Proceed* dua kali (frontend & API).

---

## 📁 Struktur Repository

```
rainshop/
├── app/                  # Backend FastAPI
│   ├── models/           #   ORM models (SQLAlchemy)
│   ├── schemas/          #   Pydantic request/response
│   ├── crud/             #   Database operations
│   ├── routers/          #   API endpoints
│   └── utils/
│       └── image_helper.py  # ResNet50 + FAISS core
├── client/               # Frontend Vue.js (source)
│   └── src/
│       ├── views/        #   Halaman: POS, item-list, item-form, search
│       └── components/   #   CameraCapture (1, 2, 3 versi)
├── webapp/               # Frontend build production
├── migrations/           # Alembic database migrations
├── db_script/
│   └── rainshop_schema.sql  # Schema lengkap (single file)
├── rainshop.bat          # One-click launcher
└── build-client.bat      # Build frontend → webapp/
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

## 🤝 Kontribusi & Kontak

Proyek ini dikembangkan untuk toko **Rain Shop** — toko pernak-pernik di Bojong Gede, Bogor.

Tertarik berdiskusi tentang proyek ini?  
📧 [alaric2001ra@gmail.com](mailto:alaric2001ra@gmail.com)  
🐙 [github.com/alaric2001](https://github.com/alaric2001)
