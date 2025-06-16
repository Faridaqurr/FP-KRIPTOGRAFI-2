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

# 🖋️ Fitur Watermark

## Deskripsi
Menambahkan teks watermark semi-transparan pada gambar secara otomatis di sudut kanan bawah.

## Fitur Utama
- **Posisi otomatis**: Sudut kanan bawah dengan margin 20px
- **Ukuran responsif**: Font menyesuaikan ukuran gambar
- **Semi-transparan**: 50% transparansi warna merah
- **Multi-format**: Mendukung PNG, JPG, JPEG

## Cara Kerja

### 1. Konversi Format
```python
watermark = image.convert("RGBA")  # Untuk transparansi
```

### 2. Buat Layer Teks
```python
txt_layer = Image.new("RGBA", watermark.size, (255, 255, 255, 0))
```

### 3. Hitung Ukuran Font
```python
font_size = int(min(width, height) / 20)  # 1/20 dari dimensi terkecil
```

### 4. Posisi Teks
```python
x, y = width - textwidth - 20, height - textheight - 20  # Sudut kanan bawah
```

### 5. Render Watermark
```python
draw.text((x, y), text, font=font, fill=(255, 0, 0, 128))  # Merah 50% transparan
```

## Penggunaan

### Di Streamlit
```python
watermarked = add_watermark(image, "Nama - NIM - Kelas")
```

### Standalone
```python
from watermark import add_watermark
from PIL import Image

img = Image.open("gambar.png")
result = add_watermark(img, "Watermark Text")
result.save("output.png")
```

## Spesifikasi

| Aspek | Detail |
|-------|--------|
| **Posisi** | Sudut kanan bawah (margin 20px) |
| **Warna** | Merah (#FF0000) |
| **Transparansi** | 50% (alpha=128) |
| **Font** | Arial (fallback: default) |
| **Ukuran Font** | 1/20 dimensi terkecil gambar |

## Dependencies
```
PIL (Pillow) - Image processing
```

## Contoh Penggunaan
- Tugas kuliah: "Nama - 123456789 - Kelas A"
- Foto pribadi: "© 2024 Your Name"
- Dokumen: "CONFIDENTIAL"

## PROGRAM LAIN
