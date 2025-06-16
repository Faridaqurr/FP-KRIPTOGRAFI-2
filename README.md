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

## Penghitung PSNR (Peak Signal-to-Noise Ratio) dengan Python
Proyek ini menyediakan fungsi Python sederhana untuk menghitung **PSNR (Peak Signal-to-Noise Ratio)** antara dua gambar menggunakan pustaka `PIL (Pillow)` dan `NumPy`. PSNR biasa digunakan untuk mengukur kualitas gambar hasil kompresi atau rekonstruksi dibandingkan dengan gambar aslinya.

### Fitur

- Menerima dua input gambar (berformat `PIL.Image`).
- Mengubah ukuran gambar kedua agar sama dengan gambar pertama.
- Mengonversi kedua gambar menjadi RGB untuk konsistensi.
- Mengembalikan nilai PSNR dalam satuan desibel (dB).


### Apa Itu PSNR?
**PSNR (Peak Signal-to-Noise Ratio)** adalah ukuran kualitas gambar hasil kompresi atau manipulasi dibandingkan dengan gambar aslinya. Nilai PSNR yang lebih tinggi menunjukkan kualitas gambar yang lebih baik (lebih mirip dengan aslinya).

Rumus PSNR:

![image](https://github.com/user-attachments/assets/f101cd9f-4fbd-4cce-8f78-1da7492f9a90)


- `MAX_I` adalah nilai maksimum piksel (biasanya 255 untuk gambar 8-bit).
- `MSE` adalah *Mean Squared Error* atau rata-rata dari selisih kuadrat antara dua gambar.


## SELAIN PNSR APA
