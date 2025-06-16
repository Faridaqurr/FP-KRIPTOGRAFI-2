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

# Visual Crypto
Modul ini mengimplementasikan teknik *Visual Cryptography* untuk gambar hitam-putih. Visual cryptography memungkinkan pembagian gambar rahasia menjadi dua bagian acak (share) yang tidak dapat dimengerti secara terpisah. Namun, jika kedua bagian digabungkan, gambar asli dapat direkonstruksi secara visual.
## Fitur
- Membuat dua share acak dari gambar biner (mode '1').
- Mereproduksi kembali gambar asli dengan menggabungkan kedua share.
- Menggunakan pola 2x2 piksel untuk ekspansi piksel dan menyimpan informasi visual.
## Struktur Pola
Modul menggunakan pola 2x2 piksel untuk mewakili satu piksel dari gambar asli. Pola-pola ini dibagi menjadi dua jenis:
- Pola untuk *putih* (informasi visual tidak disembunyikan)
- Pola untuk *hitam* (menggunakan kombinasi saling melengkapi antar share)
Setiap jenis pola memiliki beberapa varian untuk meningkatkan keamanan melalui kerandoman.
## Fungsi
### create_shares(image)
Membagi gambar hitam-putih menjadi dua share acak.
*Parameter:*
- image (PIL.Image.Image): Gambar sumber yang harus dalam mode '1' (hitam-putih). Jika belum, akan dikonversi.
*Output:*
- Tuple (share1, share2) berupa dua gambar yang masing-masing merupakan hasil ekspansi dan enkripsi visual dari gambar asli.
*Proses:*
- Setiap piksel asli (1 piksel) diubah menjadi 2x2 blok piksel.
- Blok dipilih acak dari pola-pola sesuai warna piksel.
- Share 1 dan Share 2 masing-masing menerima pola berbeda yang jika digabungkan akan menghasilkan kembali representasi piksel asli.
---

### combine_shares(share1, share2)
Menggabungkan dua share untuk merekonstruksi gambar asli.
*Parameter:*
- share1 (PIL.Image.Image): Share pertama.
- share2 (PIL.Image.Image): Share kedua.
*Output:*
- PIL.Image.Image: Gambar hasil rekonstruksi dalam mode '1'.
*Proses:*
- Melakukan operasi logika minimum pada setiap piksel (AND visual).
- Jika salah satu share berisi piksel hitam (0), maka hasilnya juga hitam.
- Ini meniru efek tumpang tindih dua lembar transparansi.
---

## Contoh Penggunaan
```python
from PIL import Image
from visual_crypto import create_shares, combine_shares
# Load gambar biner
original = Image.open("secret_bw.png").convert("1")
# Buat dua share
share1, share2 = create_shares(original)
share1.save("share1.png")
share2.save("share2.png")
# Gabungkan share untuk melihat hasil rekonstruksi
result = combine_shares(share1, share2)
result.save("reconstructed.png")

## STEGANOGRAFI

`stegano.py` adalah modul Python yang memungkinkan pengguna untuk **menyisipkan teks atau gambar rahasia ke dalam gambar lain** (cover image) menggunakan teknik **Least Significant Bit (LSB)**. Versi ini menggunakan **buffer dan delimiter unik** untuk menjamin ekstraksi pesan secara aman dan akurat.


## Fitur

- Menyembunyikan **teks** dalam gambar.
- Menyembunyikan **gambar biner (hitam-putih)** dalam gambar.
- Menggunakan **delimiter 3-byte unik** sebagai penanda akhir pesan.
- Dapat mengembalikan pesan atau gambar yang disisipkan dengan akurat.
- Implementasi dengan buffer untuk ekstraksi bit yang efisien dan aman.


## Cara Kerja Singkat

- Setiap piksel RGB menyimpan **3 bit pesan rahasia**: 1 di R, 1 di G, dan 1 di B.
- Setelah semua bit pesan disisipkan, ditambahkan **delimiter**: `111111111111000000001111`.
- Saat membaca kembali, proses ekstraksi terus berjalan hingga **delimiter** ditemukan.
- Untuk gambar, dimasukkan metadata (ukuran gambar) di awal stream.

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

## Fitur Watermarking

## Deskripsi
Fitur watermarking pada Tab 3 aplikasi Kriptografi Media Suite yang menambahkan teks identitas semi-transparan pada gambar secara otomatis.

## Cara Kerja di Streamlit

### 1. Interface User
```python
with tab3:
    st.subheader("🖋️ Tambahkan Watermark ke Gambar")
    wm_file = st.file_uploader("📥 Upload Gambar", type=["png", "jpg", "jpeg"], key="wm")
    watermark_text = st.text_input("✍️ Teks Watermark (Contoh: Nama/NIM/Kelas)")
```

**Input yang diperlukan:**
- **File gambar**: Format PNG, JPG, atau JPEG
- **Teks watermark**: String bebas (nama, NIM, kelas, dll)

### 2. Processing Logic
```python
if wm_file and watermark_text:
    try:
        img = Image.open(wm_file)
        watermarked = add_watermark(img, watermark_text)
        st.image(watermarked, caption="📌 Gambar dengan Watermark", use_container_width=True)
        
        buf = io.BytesIO()
        watermarked.save(buf, format="PNG")
        st.download_button("⬇️ Unduh Gambar Watermark", buf.getvalue(), file_name="watermarked.png")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
```

**Alur proses:**
1. **Validasi input**: Cek file dan teks tersedia
2. **Load gambar**: Buka file menggunakan PIL
3. **Apply watermark**: Panggil fungsi `add_watermark()`
4. **Preview**: Tampilkan hasil di interface
5. **Download**: Siapkan buffer untuk download
6. **Error handling**: Tangkap dan tampilkan error

## Fungsi Core: `add_watermark()`

### Parameter
- `image`: Object PIL Image
- `text`: String teks watermark

### Step-by-Step Implementation

#### 1. Persiapan Canvas
```python
watermark = image.convert("RGBA")
width, height = watermark.size
```
- Convert ke RGBA untuk support transparansi
- Ambil dimensi gambar untuk perhitungan posisi

#### 2. Buat Layer Transparan
```python
txt_layer = Image.new("RGBA", watermark.size, (255, 255, 255, 0))
draw = ImageDraw.Draw(txt_layer)
```
- Layer baru dengan background transparan penuh
- Object drawing untuk render teks

#### 3. Setup Font
```python
font_size = int(min(width, height) / 20)
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except:
    font = ImageFont.load_default()
```
- Ukuran font = 1/20 dari dimensi terkecil
- Fallback ke font default jika Arial tidak ada

#### 4. Hitung Posisi
```python
bbox = draw.textbbox((0, 0), text, font=font)
textwidth = bbox[2] - bbox[0]
textheight = bbox[3] - bbox[1]
x, y = width - textwidth - 20, height - textheight - 20
```
- Gunakan `textbbox()` untuk akurasi pengukuran
- Posisi 20 pixel dari sudut kanan bawah
- Mencegah teks terpotong

#### 5. Render Watermark
```python
draw.text((x, y), text, font=font, fill=(255, 0, 0, 128))
```
- Warna merah (#FF0000) dengan alpha 128 (50% transparan)
- Posisi sudah dihitung sebelumnya

#### 6. Gabung Layer
```python
combined = Image.alpha_composite(watermark, txt_layer)
return combined.convert("RGB")
```
- Composite layer watermark dengan layer teks
- Convert ke RGB untuk compatibility

## Spesifikasi Teknis

| Parameter | Nilai | Keterangan |
|-----------|-------|------------|
| **Posisi** | Kanan bawah | Margin 20px dari tepi |
| **Warna** | Merah (#FF0000) | Kontras tinggi |
| **Transparansi** | 50% (alpha=128) | Balance visible-subtle |
| **Font Size** | min(w,h)/20 | Responsif ukuran gambar |
| **Font** | Arial → Default | Fallback otomatis |
| **Format Output** | PNG | Via BytesIO buffer |

## User Experience

### Input Validation
- **File types**: PNG, JPG, JPEG supported
- **Required fields**: File dan teks harus diisi
- **Real-time preview**: Hasil langsung ditampilkan

### Output Features
- **Preview image**: Tampilan container width penuh
- **Download button**: Otomatis muncul setelah processing
- **File naming**: "watermarked.png" sebagai default

### Error Handling
- **Try-catch wrapper**: Semua error tertangkap
- **User-friendly message**: Error dengan emoji dan format jelas
- **Graceful failure**: Aplikasi tetap berjalan meski ada error

## Contoh Penggunaan

### Akademik
```
Input text: "John Doe - 1234567890 - Kelas A"
```

### Professional  
```
Input text: "© 2024 Company Name"
```

### Personal
```
Input text: "My Photography"
```