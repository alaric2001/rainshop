# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Gambaran Umum

Repository ini berisi **dua aplikasi** yang saling terintegrasi untuk sistem POS (Point of Sale) toko Rainshop:

1. **`app/`** (root repo) — Backend REST API dengan FastAPI (Python)
2. **`client/`** — Frontend source code Vue.js 2
3. **`webapp/`** — Hasil build production frontend (dijalankan via `http-server`)

Fitur unggulan: pencarian item barang menggunakan **AI image similarity search** (FAISS + ResNet50) — kasir cukup arahkan kamera ke barang, tanpa perlu kode barcode.

Untuk menjalankan kedua aplikasi sekaligus, klik **`rainshop.bat`** di root repo.

---

## Struktur Root Repo

```
rainshop/
├── app/                  # Kode backend FastAPI
│   ├── .env              # Konfigurasi DB (tidak di-commit, lihat .env.example)
│   └── .env.example      # Template — salin ke .env lalu isi password
├── client/               # Source code frontend Vue.js 2
│   ├── .env.example           # Template env development
│   └── .env.production.example # Template env production (ngrok URL)
├── webapp/               # Build production frontend (hasil npm run build)
├── migrations/           # Alembic database migrations
├── db_script/
│   └── rainshop_schema.sql  # Schema lengkap (single file, fresh install)
├── libusb-1.0.29/        # DLL untuk thermal printer USB
├── img/                  # Gambar item barang (auto-generated, tidak di-commit)
├── index_barang.bin      # FAISS index (auto-generated, tidak di-commit)
├── cert.pem              # SSL certificate self-signed (tidak di-commit)
├── key.pem               # SSL private key (tidak di-commit)
├── alembic.ini           # Konfigurasi Alembic
├── requirements.txt      # Dependensi Python
├── rainshop.bat          # Launcher: backend + frontend + ngrok + buka browser
└── build-client.bat      # Build frontend dan copy ke webapp/
```

---

## Backend (root repo / `app/`)

### Menjalankan

```powershell
# Dari root repo — uvicorn HARUS dijalankan dari root
uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile key.pem --ssl-certfile cert.pem --reload
```

API berjalan di `https://127.0.0.1:8000`. Dokumentasi Swagger: `https://127.0.0.1:8000/docs`.

### Setup pertama kali

```powershell
pip install -r requirements.txt
```

Setelah install library baru:
```powershell
pip freeze > requirements.txt
```

### Konfigurasi Database

Salin `app/.env.example` → `app/.env` lalu isi:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=rainshop
```
File `app/.env` tidak di-commit (ada di `.gitignore`).

### Arsitektur Backend

```
app/
├── main.py          # Entry point, registrasi router & middleware CORS
├── database.py      # SQLAlchemy engine, SessionLocal, Base
├── config.py        # Baca .env, ekspos DB_* dan PRINTER_LIBUSB_PATH
├── models/          # ORM models: ItemBarang, ItemImage, SalesHeader, SalesLine, VwItemBarang
├── schemas/         # Pydantic schemas request/response
├── crud/            # Logika database (query, insert, update)
├── routers/         # FastAPI router endpoints
└── utils/
    ├── image_helper.py  # ResNet50 + FAISS: preprocess_image, faiss_write, faiss_search
    └── bluetooth.py
```

### Router Endpoints

| Router | Prefix | Fungsi |
|--------|--------|--------|
| `itembarang.py` | `/items` | CRUD item, search by name, search by image (FAISS) |
| `item_images.py` | `/images` | Upload/update gambar item |
| `sales.py` | `/sales` | Simpan transaksi penjualan |
| `print.py` | `/print-struk` | Cetak struk ke thermal printer USB |
| `voiceover.py` | `/voiceover` | Generate audio dengan gTTS |

### Sistem AI Image Search (FAISS)

- Model **ResNet50** (ImageNet weights, `pooling="avg"`) dimuat sekali saat startup → vektor 2048 dimensi.
- Index FAISS: file **`index_barang.bin`** di root repo.
- Gambar item: folder **`img/`** di root repo.
- Setiap item punya hingga 3 gambar, masing-masing punya `faiss_index` unik di tabel `item_images`.
- `faiss_index` di DB dan file `.bin` harus selalu sinkron — jangan edit `.bin` manual.

### Thermal Printer

- **python-escpos** via USB (vendor `0x0483`, product `0x070b`).
- `libusb-1.0.dll` di-resolve dari `libusb-1.0.29/VS2022/MS64/dll/libusb-1.0.dll` oleh `config.py`.
- Endpoint: `POST /print-struk`.

---

## Frontend: `client/` → `webapp/`

### Alur Build

```powershell
# Development (hot-reload)
cd client
npm run serve

# Build lokal (untuk LAN) → copy ke webapp/
build-client.bat

# Deploy ke GitHub Pages (production)
cd client
npm run deploy
```

`client/vue.config.js`:
- Development: `publicPath: ''`
- Production: `publicPath: '/rainshop/'` (GitHub Pages repo name)
- `outputDir: 'dist'` — bukan langsung ke `webapp/` karena bisa terkunci oleh http-server

### Konfigurasi API URL

`client/src/main.js`:
```javascript
// Production (GitHub Pages): pakai VUE_APP_BASE_API dari .env.production (ngrok URL)
// Development / LAN: ikut hostname browser secara dinamis
axios.defaults.baseURL = process.env.NODE_ENV === 'production'
    ? process.env.VUE_APP_BASE_API
    : `${window.location.protocol}//${window.location.hostname}:8000`;
```

File env frontend (semua **tidak di-commit**, ada template `.example`-nya):
- `client/.env` — development: `VUE_APP_BASE_API=http://127.0.0.1:8000`
- `client/.env.production` — production: `VUE_APP_BASE_API=https://<ngrok-domain>`

### Arsitektur Frontend

```
client/src/
├── main.js           # Setup Vue, axios baseURL, plugin global
├── routes.js         # Vue Router — urutan: /item-input, /item-list, /search, /penjualan
├── store.js          # Vuex store (termasuk state stream kamera)
├── App.vue           # Bottom navigation bar (fixed, z-index: 9999)
├── apis/
│   ├── items.js      # Axios calls ke /items dan /images
│   └── sales.js      # Axios calls ke /sales dan /print-struk
├── components/
│   ├── CameraCapture.vue   # Kamera tunggal + tombol Ambil (orderfrm, SearchItem)
│   ├── CameraCapture2.vue  # Kamera tunggal sederhana (item-form edit gambar)
│   ├── CameraCapture3.vue  # Kamera 3 tombol Foto#1/2/3 (item-form input baru)
│   ├── calculator.vue
│   └── my-number.vue       # Input angka dengan format separator
└── views/
    ├── item-form.vue    # Input barang baru: kamera → preview foto → data barang
    ├── item-list.vue    # Daftar & manajemen barang, edit nama/harga/stok/gambar
    ├── SearchItem.vue   # Cari barang dengan kamera (standalone)
    └── orderfrm.vue     # POS utama: cari item + keranjang belanja + pembayaran
```

### Halaman & Routes

| Route | View | Fungsi |
|-------|------|--------|
| `/` | redirect → `/penjualan` | Default |
| `/item-input` | `item-form.vue` | Tambah barang baru |
| `/item-list` | `item-list.vue` | Daftar & edit barang |
| `/search` | `SearchItem.vue` | Cari barang pakai kamera |
| `/penjualan` | `orderfrm.vue` | Transaksi POS |

### Komponen Kamera

Semua komponen kamera menggunakan:
```javascript
navigator.mediaDevices.getUserMedia({
  video: { facingMode: { ideal: 'environment' }, aspectRatio: { ideal: 16/9 } }
})
```
- `ideal: 'environment'` — utamakan kamera belakang HP, fallback ke kamera apapun di PC
- `aspectRatio: 16/9` — tampilan kamera menyerupai webcam
- Video di-render dengan `aspect-ratio: 16/9` + `object-fit: cover` via CSS

**Kamera hanya bekerja di HTTPS atau localhost.** Di LAN via IP → pakai self-signed cert. Dari internet → pakai ngrok (otomatis HTTPS).

### Desain UI

- **Light mode** — primary color `#2563eb` (biru), background `#f1f5f9`
- **Mobile-first** — layout responsif, bottom navigation bar (z-index: 9999)
- `html, body { overflow-x: hidden }` — wajib agar `position: fixed` bottom-nav tidak bergeser saat ada horizontal overflow
- `orderfrm.vue`: tab switcher mobile (Cari Barang | Keranjang), side-by-side di desktop
- Kamera dan hasil pencarian menggunakan layout dua kolom yang sama di semua halaman (`flex: 1 1 340px` / `flex: 1 1 280px`)

---

## HTTPS & Deployment

### Mode LAN (akses dari HP di WiFi yang sama)

Self-signed certificate — generate sekali:
```powershell
$openssl = "C:\Program Files\Git\usr\bin\openssl.exe"
& $openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 825 -nodes `
  -subj "/CN=rainshop-local/O=Rainshop/C=ID" `
  -addext "subjectAltName=IP:192.168.1.15,IP:127.0.0.1,DNS:localhost"
```
Ganti `192.168.1.15` dengan IP lokal PC. `cert.pem` dan `key.pem` di-ignore git.

Akses dari HP (pertama kali): buka `https://[IP]:8000` → Proceed, lalu `https://[IP]:8080` → Proceed.

### Mode Internet (GitHub Pages + ngrok)

Frontend di-host di **GitHub Pages**: `https://alaric2001.github.io/rainshop/`

Backend di-expose via **ngrok static domain** (URL tidak berubah meski ngrok di-restart):
```powershell
# Setup sekali
ngrok config add-authtoken <TOKEN>

# Jalankan setiap demo (sudah otomatis di rainshop.bat)
ngrok http --domain=cube-judicial-amber.ngrok-free.dev https://localhost:8000
```

Setelah ganti ngrok domain, update `client/.env.production` lalu:
```powershell
cd client && npm run deploy
```

---

## Database (MySQL)

### Schema Lengkap (Fresh Install)

Jalankan **satu file ini** pada database kosong:
```
db_script/rainshop_schema.sql
```

Objek yang dibuat:
| Objek | Tipe | Keterangan |
|-------|------|------------|
| `itembarang` | Tabel | Master barang — item_id, nama, harga, stok, isactive, image_id, modified |
| `item_images` | Tabel | Gambar per barang, tiap baris punya `faiss_index` unik |
| `sales_header` | Tabel | Header transaksi penjualan |
| `sales_line` | Tabel | Detail baris transaksi |
| `vw_itembarang` | View | Join itembarang + item_images, dipakai FAISS search |
| `vw_sales_line` | View | Join sales_line + itembarang untuk detail transaksi |
| `usp_sales_nomorbaru` | Procedure | Generate nomor transaksi otomatis (format S2506-0001) |

### Migrasi dengan Alembic

```
migrations/
├── env.py           # Baca app/.env, import semua model, exclude view dari autogenerate
├── versions/        # File migrasi (satu file per perubahan skema)
└── script.py.mako
alembic.ini          # URL DB diisi otomatis dari migrations/env.py
```

**Perintah:**
```powershell
alembic current                                        # versi DB saat ini
alembic revision --autogenerate -m "nama_perubahan"   # buat migrasi baru
alembic upgrade head                                   # terapkan ke DB
alembic downgrade -1                                   # rollback satu versi
alembic stamp head                                     # tandai DB sudah di versi head
```

**Alur kerja:**
1. Ubah model di `app/models/`
2. `alembic revision --autogenerate -m "..."` → review file yang dibuat
3. `alembic upgrade head` → terapkan ke database

View dan stored procedure **tidak** di-track Alembic — dikelola manual via `db_script/rainshop_schema.sql`.

---

## Catatan Penting

- Uvicorn **harus dijalankan dari root repo** agar path `img/` dan `index_barang.bin` benar.
- Library `gtts` wajib terinstall — jika tidak, backend gagal start dengan `ModuleNotFoundError`.
- Jangan jalankan `npm run build` saat `http-server` sedang melayani `webapp/` — folder terkunci (`EBUSY`). Gunakan `build-client.bat`.
- Log `GET /.well-known/appspecific/com.chrome.devtools.json 404` dan `.js.map` adalah normal — bukan error.
- `client/.env` dan `client/.env.production` **tidak di-commit** — salin dari file `.example` masing-masing.
