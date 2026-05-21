# Rainshop — Sistem POS Toko Pernak-Pernik

Sistem Point of Sale dengan fitur pencarian barang menggunakan **kamera + AI** (tanpa barcode).  
Kasir cukup arahkan barang ke kamera — sistem mengenali barang secara otomatis menggunakan FAISS + ResNet50.

---

## Struktur Repo

```
rainshop/
├── app/              ← Backend FastAPI (Python)
├── client/           ← Frontend Vue.js 2 (source code)
├── webapp/           ← Frontend build hasil (static, dijalankan http-server)
├── db_script/        ← Script SQL untuk setup database MySQL
├── libusb-1.0.29/    ← DLL untuk thermal printer USB
├── img/              ← Gambar item (dibuat otomatis, tidak di-commit)
├── index_barang.bin  ← FAISS index (dibuat otomatis, tidak di-commit)
├── requirements.txt  ← Dependensi Python
└── rainshop.bat      ← Launcher: jalankan backend + frontend + buka browser
```

---

## Cara Menjalankan (Pertama Kali)

### 1. Setup Database MySQL

Jalankan script SQL berikut secara berurutan dari folder `db_script/2025-07-29/`:

```
00 rainshop.sql          ← Buat tabel & view utama
01 vw_itembarang.sql     ← View untuk FAISS search
02 ALTER itembarang ...  ← Tambah kolom image_id
03 CREATE TABLE sales... ← Tabel transaksi
04 usp_sales_nomorbaru.. ← Stored procedure nomor transaksi
```

### 2. Konfigurasi Backend

Buat file `app/.env` dengan isi:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=rainshop
```

### 3. Install Dependensi Python

```powershell
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

Klik dua kali **`rainshop.bat`** — akan membuka dua terminal (backend & frontend) dan browser secara otomatis.

Atau jalankan backend manual dari root repo:

```powershell
uvicorn app.main:app --reload
```

---

## Pengembangan Frontend

Source code Vue.js ada di `client/`. Folder `webapp/` adalah hasil build production yang dilayani oleh `http-server` saat `rainshop.bat` dijalankan.

```powershell
cd client
npm install        # hanya pertama kali
npm run serve      # development dengan hot-reload (port 8081)
npm run build      # build production → output ke ../webapp/
```

Konfigurasi URL API ada di `client/.env`:

```
VUE_APP_BASE_API=http://127.0.0.1:8000
```

---

## Update Dependensi Python

Jika menginstall library baru dengan `pip install`, update `requirements.txt`:

```powershell
pip freeze > requirements.txt
```
