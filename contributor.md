# Kontributor Proyek dan Pembagian Tugas

Berikut adalah daftar kontributor dalam proyek ini beserta penjelasan singkat mengenai tugas utama yang dikerjakan.

### 1. **Abid Ubaidillah** 
**NRP: 5027231089** <br>
**Peran:** Koordinator Proyek & Dokumentasi  
**Tugas:**
- Merancang struktur proyek dan integrasi antar modul.
- Menulis dokumentasi proyek (`README.md`, `CONTRIBUTORS.md`, dsb).
- Melakukan validasi akhir terhadap hasil integrasi semua fitur.


### 2. **Farida Qurrotu A'yuna** 
**NRP: 5027231015**<br>
**Peran:** Developer Steganografi  
**File Utama:** `stegano.py`  
**Tugas:**
- Implementasi metode encoding dan decoding teks/gambar dalam citra.
- Penggunaan teknik LSB dengan delimiter sebagai penanda akhir data.
- Mengembangkan logika buffer pada decoding untuk keandalan ekstraksi data.


### 3. **Chelsea Vania Hariyono** 
**NRP: 5027231003** <br>
**Peran:** Developer Visual Cryptography  
**File Utama:** `visual_crypto.py`  
**Tugas:**
- Menerapkan metode enkripsi visual berbasis pembagian share 2x2.
- Menjamin kompatibilitas ukuran dan format gambar hitam-putih.
- Menyediakan fungsi untuk menggabungkan dua share menjadi citra akhir.


### 4. **Malvin Putra Rismahardian** 
**NRP: 5027231048**<br>
**Peran:** Developer Kriptografi AES  
**File Utama:** `aes_crypto.py`  
**Tugas:**
- Mengimplementasikan enkripsi dan dekripsi menggunakan AES.
- Menjamin keamanan pesan dengan pengelolaan kunci simetris.
- Integrasi fitur dengan `app.py`.


### 5. **Muhammad Kenas Galeno Putra** 
**NRP: 5027231069** <br>
**Peran:** Pengembang Watermarking  
**File Utama:** `watermark.py`  
**Tugas:**
- Menyisipkan watermark ke dalam citra secara permanen.
- Menyediakan fitur ekstraksi watermark dari citra digital.
- Berkoordinasi dengan pengembang metrik evaluasi.


### 6. **Salsabila Rahmah** 
**NRP: 5027231005**<br>
**Peran:** Evaluasi Kualitas Gambar  
**File Utama:** `metrics.py`  
**Tugas:**
- Menyusun metrik PSNR dan SSIM untuk mengevaluasi hasil modifikasi gambar.
- Menganalisis dampak dari proses steganografi, watermarking, dan kriptografi.
- Memberi masukan terhadap kualitas visual output.


### 7. **Revalina Fairuzy Azhari Putri** 
**NRP: 5027231001**<br>
**Peran:** Integrasi dan Antarmuka  
**File Utama:** `app.py`  
**Tugas:**
- Mengintegrasikan seluruh fitur ke dalam satu antarmuka utama.
- Mengatur alur penggunaan mulai dari input hingga output hasil akhir.
- Menangani error, logging, dan antarmuka pengguna CLI/GUI jika ada.
