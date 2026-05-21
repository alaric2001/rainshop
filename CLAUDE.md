# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Gambaran Umum

Repository ini berisi **dua aplikasi** yang saling terintegrasi untuk sistem POS (Point of Sale) toko Rainshop:

1. **`app/`** (root repo) — Backend REST API dengan FastAPI (Python)
2. **`client/`** — Frontend webapp dengan Vue.js 2

Fitur unggulan: pencarian item barang menggunakan **AI image similarity search** (FAISS + ResNet50) — kasir cukup arahkan kamera ke barang, tanpa perlu kode barcode.

Untuk menjalankan kedua aplikasi sekaligus, cukup klik **`rainshop.bat`** di root repo.

---

## Backend (root repo / `app/`)

### Setup & Menjalankan

```powershell
# Buat virtual environment (hanya pertama kali, dari root repo)
python -m venv venv

# Aktifkan venv
venv\scripts\activate.ps1

# Install dependencies
pip install -r requirements.txt

# Jalankan API dari root repo
uvicorn app.main:app --reload
```

API berjalan di `http://127.0.0.1:8000`. Dokumentasi Swagger tersedia di `http://127.0.0.1:8000/docs`.

### Update requirements setelah install library baru

```powershell
pip freeze > requirements.txt
```

### Konfigurasi Database

File `.env` ada di `app/.env` (root repo):

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=12345
DB_NAME=rainshop
```

### Arsitektur Backend

```
app/                 # Seluruh kode backend ada di sini (root repo)
├── main.py          # Entry point, registrasi router & middleware CORS
├── database.py      # SQLAlchemy engine, SessionLocal, Base
├── config.py        # Baca .env, ekspos DB_* dan PRINTER_LIBUSB_PATH
├── models/          # SQLAlchemy ORM models (ItemBarang, ItemImage, SalesHeader, SalesLine)
├── schemas/         # Pydantic schemas untuk validasi request/response
├── crud/            # Logika database (query, insert, update)
├── routers/         # FastAPI router endpoints
└── utils/
    ├── image_helper.py  # ResNet50 + FAISS: preprocess_image, faiss_write, faiss_search
    └── bluetooth.py
```

### Router Endpoints

| Router | Prefix | Fungsi |
|--------|--------|--------|
| `itembarang.py` | `/items` | CRUD item barang, search by name, search by image (FAISS) |
| `item_images.py` | `/images` | Upload/update gambar item |
| `sales.py` | `/sales` | Simpan transaksi penjualan |
| `print.py` | `/print-struk` | Cetak struk ke thermal printer USB |
| `voiceover.py` | `/voiceover` | Generate audio voiceover dengan gTTS |

### Sistem AI Image Search (FAISS)

- Model **ResNet50** (ImageNet weights, pooling="avg") dimuat sekali saat startup, menghasilkan vektor 2048 dimensi per gambar.
- Index FAISS disimpan sebagai file **`index_barang.bin`** di root repo (direktori kerja saat `uvicorn` dijalankan).
- Gambar item disimpan di folder **`img/`** di root repo.
- Setiap item bisa punya hingga 3 gambar; masing-masing punya `faiss_index` unik yang tersimpan di tabel `item_images`.
- Field `faiss_index` di database dan di file `.bin` harus selalu sinkron — jangan manipulasi file `.bin` secara manual.

### Thermal Printer

- Menggunakan **python-escpos** via USB (vendor `0x0483`, product `0x070b`).
- Memerlukan **libusb-1.0.dll** — path-nya di-resolve oleh `config.py` ke `libusb-1.0.29/VS2022/MS64/dll/libusb-1.0.dll`.
- Printer diakses di endpoint `POST /print-struk`.

---

## Frontend: client/

### Setup & Menjalankan

```powershell
cd client
npm install
npm run serve    # Development server (hot-reload)
npm run build    # Build untuk production
npm run lint     # Lint code
```

### Konfigurasi API

File `client/.env`:
```
VUE_APP_BASE_API=http://127.0.0.1:8000
```

Axios `baseURL` dikonfigurasi di `main.js` menggunakan `process.env.VUE_APP_BASE_API`.

### Arsitektur Frontend

`webapp/` adalah folder **hasil build production** dari `client/`. Dikonfigurasi di `client/vue.config.js` dengan `outputDir: '../webapp'`. Dijalankan via `http-server` oleh `rainshop.bat`.

```
client/src/
├── main.js        # Setup Vue, axios baseURL, plugin (BootstrapVue, vue-moment, dll)
├── routes.js      # Definisi route Vue Router
├── store.js       # Vuex store
├── apis/
│   ├── items.js   # Axios calls ke /items dan /images
│   └── sales.js   # Axios calls ke /sales
└── views/
    ├── orderfrm.vue    # Halaman utama POS — cari item (kamera/nama) + keranjang belanja
    ├── item-list.vue   # Daftar & manajemen item barang
    ├── item-form.vue   # Form tambah/edit item dengan upload foto kamera
    └── SearchItem.vue  # Halaman pencarian item
```

### Halaman & Routes

| Route | View | Fungsi |
|-------|------|--------|
| `/` | redirect ke `/penjualan` | Default |
| `/penjualan` | `orderfrm.vue` | Transaksi POS utama |
| `/item-list` | `item-list.vue` | Manajemen barang |
| `/item-input` | `item-form.vue` | Tambah/edit barang |
| `/search` | `SearchItem.vue` | Pencarian barang |

---

## Database (MySQL)

Script SQL ada di `db_script/2025-07-29/`. Skema utama:

- **`itembarang`** — master data barang (item_id UUID, nama, harga, stok, isactive)
- **`item_images`** — gambar per barang, tiap baris punya `faiss_index` unik
- **`sales_header`** + **`sales_line`** — transaksi penjualan
- **`vw_itembarang`** — view join `itembarang` + `item_images` (dipakai untuk FAISS search)
- **`vw_sales_line`** — view untuk detail transaksi
- **`usp_sales_nomorbaru`** — stored procedure untuk generate nomor transaksi baru

---

## Catatan Penting

- Uvicorn **harus dijalankan dari root repo** agar path `img/` dan `index_barang.bin` benar. Jika dijalankan dari folder lain, FAISS index dan gambar item tidak akan ditemukan.
- Library `gtts` wajib terinstall di environment Python yang dipakai (`pip install gtts`) — jika tidak, backend gagal start dengan `ModuleNotFoundError`.
- File `rainshop.bat` menjalankan backend (uvicorn) dan frontend (http-server dari folder `webapp/`) sekaligus, lalu membuka Edge otomatis setelah 45 detik.
