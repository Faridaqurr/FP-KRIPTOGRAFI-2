# FP KRIPTOGRAFI KELOMPOK 2

Anggota Kelompok :

|Nama|NRP|
|---|---|
|Revalina Fairuzy Azhari P.|5027231001|
|Chelsea Vania Hariyono|5027231003|
|Salsabila Rahmah|5027231005|
|Farida Qurrotu A.|5027231015|
|Muhammad Kenas Galeno P.|5027231069|
|Abid Ubaidillah A.|5027231089|
|Malvin Putra Rismahardian|5027231048|

## Tugas

- Mahasiswa diwajibkan untuk mengembangkan sebuah final project sebagai bentuk implementasi dari teori yang telah dipelajari.
  - Tema proyek disesuaikan dengan topik yang telah dipilih.
  - FP harus berupa aplikasi yang memiliki antarmuka pengguna (UI) yang fungsional dan relevan dengan topik yang dipilih.
  - Buat dokumentasi FP menggunakan Github Markdown (atau sejenisnya)
  - Pembagian tugas individu dapat disertakan dalam dokumentasi FP (misalnya dalam file README.md atau CONTRIBUTORS.md) dengan menyebutkan siapa mengerjakan apa (misal: frontend, backend, dokumentasi, pengujian, dsb).
 
# Penjelasan Sistem Kriptografi Visual & Enkripsi dalam Media

## PSNR PROGRAM

Proyek ini menyediakan fungsi Python untuk menghitung **PSNR (Peak Signal-to-Noise Ratio)** antara dua gambar digital — biasanya digunakan untuk membandingkan gambar asli dengan gambar hasil steganografi, kompresi, atau rekonstruksi.

### Fitur

- Menghitung nilai PSNR secara akurat menggunakan pustaka **`scikit-image`**.
- Validasi otomatis terhadap **ukuran dan mode warna** gambar (harus sama dan berformat RGB).
- Memberikan pesan kesalahan jika gambar tidak sesuai.

###  Apa Itu PSNR?

**PSNR (Peak Signal-to-Noise Ratio)** adalah metrik umum untuk mengukur kualitas rekonstruksi gambar. Biasanya digunakan untuk menilai seberapa mirip gambar hasil manipulasi (seperti steganografi atau kompresi) dengan gambar aslinya.

Rumus PSNR (yang diimplementasikan oleh `scikit-image`):

![image](https://github.com/user-attachments/assets/62c20da6-212a-4b23-bca1-6032fd8474c9)

- **MAX** adalah nilai maksimum piksel (255 untuk gambar 8-bit).
- **MSE (Mean Squared Error)** adalah rata-rata kuadrat perbedaan antar piksel gambar.


## PROGRAM LAIN
