# VillaShield

VillaShield adalah aplikasi pemesanan villa berbasis web menggunakan Python Flask dan MySQL. Aplikasi ini mendukung pemesanan villa oleh pengguna, pengelolaan pemesanan oleh admin, serta enkripsi data identitas menggunakan algoritma AES.

---
Ayesa Aglystia n Ayat Akras
Syifa Tania


## Fitur Aplikasi

### Pengguna
- Registrasi dan login
- Melakukan pemesanan villa
- Validasi tanggal dan ketersediaan nomor villa
- Enkripsi otomatis data identitas (misal: NIK)
- Melihat riwayat pemesanan
- Mengunduh tiket pemesanan dalam format PDF

### Admin
- Login sebagai admin
- Melihat seluruh daftar pemesanan
- Menambahkan pemesanan sebagai guest
- Mengubah status checkout
- Statistik jumlah pemesanan dan total pendapatan
- Grafik pemesanan per bulan
- Melihat dan menghapus user (soft delete)

---

## Instalasi & Menjalankan Aplikasi

### 1. Instalasi Software
- Install Python (disarankan versi 3.10+)
- Install XAMPP untuk menjalankan MySQL
- Jalankan Apache dan MySQL dari XAMPP

### 2. Instalasi Dependensi
Buka terminal dan jalankan:

```bash
pip install flask pycryptodome mysql-connector-python bcrypt reportlab qrcode
