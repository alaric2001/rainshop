
# Repo ini terdiri atas dua project atau dua aplikasi
### 1. Project Server API dg nama rainshop_fastapi dalam folder rainshop_fastapi
### 2. Project Client WEPAPP dg nama rainshop_web dalam folder rainshop_web

## Jika pertama kali GIT CLONE, maka lakukan berikut ini :
* Buka/buat TERMINAL > New 

* Masuk ke folder rainshop_fastapi
 `cd rainshop_fastapi`

* Buat _virtual Environment_ dengan cara jalankan command
`python -m venv venv`

* Setelah itu aktifkan venv nya, deng cara jalankan command berikut ini
`./envn/Scripts/Activate.ps1`

* kemudian lakukan instalasi semua library yg diperlukan, dengan cara jalanan command berikut ini:
`pip install -r requirements.txt`

* setelah itu jalankan api dengan command berikut ini
`uvicorn main:app --reload`

* jika anda melakukan perubahan coding dan menginstall library baru dg pip install, maka setelah jalan command berikut ini 
`pip freeze > requirements.txt`
untuk mengupdate daftar library yg dipakai dalam project rainshop_fastapi 