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
├── client/               # Source code frontend Vue.js 2
├── webapp/               # Build production frontend (hasil npm run build)
├── db_script/            # Script SQL setup database
├── libusb-1.0.29/        # DLL untuk thermal printer USB
├── img/                  # Gambar item barang (auto-generated, tidak di-commit)
├── index_barang.bin      # FAISS index (auto-generated, tidak di-commit)
├── cert.pem              # SSL certificate self-signed (tidak di-commit)
├── key.pem               # SSL private key (tidak di-commit)
├── requirements.txt      # Dependensi Python
├── rainshop.bat          # Launcher: jalankan backend + frontend + buka browser
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

File `app/.env` (tidak di-commit):
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=12345
DB_NAME=rainshop
```

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
# Development (hot-reload, tanpa HTTPS)
cd client
npm run serve

# Production build → copy ke webapp/
# Cara 1: klik build-client.bat
# Cara 2: manual
cd client
npm run build
xcopy /E /Y dist\* ..\webapp\
```

`client/vue.config.js` menggunakan `outputDir: 'dist'` (bukan langsung ke `webapp/` karena folder webapp bisa terkunci oleh http-server yang sedang berjalan). Setelah build, hasil di `client/dist/` dicopy manual ke `webapp/`.

### Konfigurasi API URL

`client/src/main.js` — URL API mengikuti protokol browser secara dinamis:
```javascript
axios.defaults.baseURL = `${window.location.protocol}//${window.location.hostname}:8000`;
```
- Akses via HTTP → API ke `http://...:8000`
- Akses via HTTPS (dari HP) → API ke `https://...:8000`

File `client/.env` sudah tidak dipakai untuk baseURL (diabaikan).

### Arsitektur Frontend

```
client/src/
├── main.js           # Setup Vue, axios baseURL dinamis, plugin global
├── routes.js         # Vue Router — urutan: /item-input, /item-list, /search, /penjualan
├── store.js          # Vuex store (termasuk state stream kamera)
├── App.vue           # Bottom navigation bar (fixed, z-index: 9999)
├── apis/
│   ├── items.js      # Axios calls ke /items dan /images
│   └── sales.js      # Axios calls ke /sales dan /print-struk
├── components/
│   ├── CameraCapture.vue   # Kamera tunggal + tombol Ambil (dipakai di orderfrm, SearchItem)
│   ├── CameraCapture2.vue  # Kamera tunggal versi sederhana (dipakai di item-form edit gambar)
│   ├── CameraCapture3.vue  # Kamera dengan 3 tombol ambil Gambar#1/2/3 (dipakai di item-form input)
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
  video: { facingMode: { ideal: 'environment' } }  // default kamera belakang HP
})
```
`ideal` berarti: utamakan kamera belakang, fallback ke kamera apapun jika tidak ada (misalnya di PC).

**Kamera hanya bekerja di HTTPS atau localhost.** Di jaringan LAN via IP, wajib pakai HTTPS.

### Desain UI

- **Light mode** — primary color `#2563eb` (biru), background `#f1f5f9`
- **Mobile-first** — layout responsif, bottom navigation bar
- `html, body { overflow-x: hidden }` — penting untuk mencegah horizontal scroll yang membuat `position: fixed` bottom-nav bergeser di mobile
- `orderfrm.vue`: tab switcher mobile (Cari Barang | Keranjang), layout side-by-side di desktop

---

## HTTPS (Akses dari Handphone)

Browser mobile memblokir akses kamera di halaman HTTP. Solusi: self-signed SSL certificate.

### Generate Certificate (hanya sekali)

Membutuhkan OpenSSL dari Git for Windows:
```powershell
$openssl = "C:\Program Files\Git\usr\bin\openssl.exe"
& $openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 825 -nodes `
  -subj "/CN=rainshop-local/O=Rainshop/C=ID" `
  -addext "subjectAltName=IP:192.168.1.15,IP:127.0.0.1,DNS:localhost"
```
Ganti `192.168.1.15` dengan IP lokal PC yang sebenarnya.

`cert.pem` dan `key.pem` di-ignore oleh git (tidak di-commit).

### Cara Akses dari HP (pertama kali)

1. Jalankan `rainshop.bat`
2. Di HP, buka `https://[IP-PC]:8000` → ketuk **Advanced → Proceed** (izinkan API)
3. Buka `https://[IP-PC]:8080` → ketuk **Advanced → Proceed** (izinkan frontend)
4. Kamera siap digunakan

---

## Database (MySQL)

Script SQL di `db_script/2025-07-29/`:

- **`itembarang`** — master data barang (item_id UUID, nama, harga, stok, isactive)
- **`item_images`** — gambar per barang, tiap baris punya `faiss_index` unik
- **`sales_header`** + **`sales_line`** — transaksi penjualan
- **`vw_itembarang`** — view join `itembarang` + `item_images` (dipakai FAISS search)
- **`vw_sales_line`** — view detail transaksi
- **`usp_sales_nomorbaru`** — stored procedure generate nomor transaksi

---

## Catatan Penting

- Uvicorn **harus dijalankan dari root repo** agar path `img/` dan `index_barang.bin` benar.
- Library `gtts` wajib terinstall (`pip install gtts`) — jika tidak, backend gagal start.
- Jangan jalankan `npm run build` saat `http-server` sedang melayani folder `webapp/` — folder akan terkunci (`EBUSY`). Gunakan `build-client.bat` yang menjalankan build ke `dist/` lalu copy.
- Log `GET /.well-known/appspecific/com.chrome.devtools.json 404` dan `.js.map` dari http-server adalah normal — bukan error.
