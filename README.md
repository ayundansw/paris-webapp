# PARIS - Praktikum Inventaris

Aplikasi manajemen inventaris barang praktikum berbasis Django, Tailwind, dan Flowbite. Dirancang untuk laboratorium, ruang praktikum, atau institusi pendidikan yang membutuhkan pencatatan barang, lokasi, dan statistik inventaris secara modern, aman, dan responsif.

## Fitur Utama
- Dashboard statistik barang masuk, stok, dan ringkasan
- CRUD data barang, lokasi, dan foto barang
- Upload foto barang saat tambah/edit
- Sistem autentikasi (register, login, profil, logout)
- Landing page promosi aplikasi
- Sidebar & navbar responsif, highlight menu aktif
- Konfirmasi sebelum logout
- Proteksi data dengan login
- Desain UI eksklusif, modern, dan mobile friendly

## Instalasi & Menjalankan
1. **Clone repo**
   ```bash
   git clone <repo-url>
   cd paris-app
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Migrasi database**
   ```bash
   python manage.py migrate
   ```
4. **Jalankan server**
   ```bash
   python manage.py runserver
   ```
5. **Akses aplikasi**
   Buka browser ke `http://localhost:8000/`

## Struktur Folder Penting
- `inventaris/` : App utama (model, views, forms, urls, template barang/lokasi)
- `accounts/`   : App autentikasi (login, register, profile)
- `templates/`  : Semua template HTML (landing, dashboard, sidebar, dsb)
- `static/`     : File statis ( img )

## Kontribusi
Pull request, issue, dan feedback sangat diterima!

## Lisensi
MIT

---

**PARIS - Praktikum Inventaris**
> Modern Inventory Management for Labs & Education

Ayunda.
Thanks~

