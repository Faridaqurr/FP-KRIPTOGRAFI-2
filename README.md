# FP KRIPTOGRAFI KELOMPOK 2

**Anggota Kelompok :**

|Nama|NRP|
|---|---|
|Revalina Fairuzy Azhari P.|5027231001|
|Chelsea Vania Hariyono|5027231003|
|Salsabila Rahmah|5027231005|
|Farida Qurrotu A.|5027231015|
|Muhammad Kenas Galeno P.|5027231069|
|Abid Ubaidillah A.|5027231089|
|Malvin Putra Rismahardian|5027231048|

## Daftar  Isi
- [Tugas](#tugas)
- [Visual Cryptography](#visual-crypto)
- [Steganography](#steganografi)
- [PSNR](#psnr-program)
- [Watermarking](#fitur-watermarking)
- [AES](#aes-256-encryption-module)
- [Integrasi dengan Steganografi](#integration-dengan-steganografi)



# Tugas

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
```

# STEGANOGRAFI

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

## Integration dengan Steganografi

Modul ini terintegrasi dengan sistem steganografi melalui `app.py`:

###  Code Integration di app.py:

```python
# Import AES functions
from aes_crypto import encrypt as aes_encrypt, decrypt as aes_decrypt

# Session state untuk menyimpan data
if 'aes_stego_img_data' not in st.session_state: 
    st.session_state.aes_stego_img_data = None
if 'aes_extracted_text_data' not in st.session_state: 
    st.session_state.aes_extracted_text_data = None
```

**Penjelasan Code:**
- Import fungsi encrypt dan decrypt dengan alias untuk menghindari konflik nama
- Inisialisasi session state Streamlit untuk menyimpan gambar stego dan teks hasil ekstraksi

### Proses Enkripsi dan Steganografi:

```python
# 1. Enkripsi teks dengan password
encrypted_b64_string = aes_encrypt(secret_text_aes, password_aes_enc)

# 2. Sembunyikan hasil enkripsi (string base64) ke dalam gambar
cover_img = Image.open(cover_aes_file)
stego_img = encode_text(cover_img, encrypted_b64_string)
st.session_state.aes_stego_img_data = stego_img
```

**Penjelasan Code:**
- **Line 2:** Enkripsi teks rahasia menggunakan password, hasilnya string Base64
- **Line 5:** Buka gambar cover yang akan digunakan untuk menyembunyikan data
- **Line 6:** Gunakan steganografi untuk menyembunyikan string Base64 terenkripsi ke dalam gambar
- **Line 7:** Simpan gambar stego hasil ke session state untuk ditampilkan/download

### Proses Ekstraksi dan Dekripsi:

```python
stego_img = Image.open(stego_aes_file)
# 1. Ekstrak string base64 dari gambar
extracted_b64_string = decode_text(stego_img)

# 2. Dekripsi string base64 dengan password
decrypted_text = aes_decrypt(extracted_b64_string, password_aes_dec)
st.session_state.aes_extracted_text_data = decrypted_text
```

**Penjelasan Code:**
- **Line 1:** Buka gambar stego yang berisi data terenkripsi
- **Line 3:** Ekstrak string Base64 terenkripsi dari gambar menggunakan steganografi
- **Line 6:** Dekripsi string Base64 menggunakan password untuk mendapatkan teks asli
- **Line 7:** Simpan teks hasil dekripsi ke session state untuk ditampilkan

**Workflow Lengkap:**
1. User memasukkan teks rahasia dan password
2. Teks dienkripsi menggunakan AES-256 → menghasilkan string Base64
3. String Base64 disembunyikan dalam gambar menggunakan steganografi
4. Untuk ekstraksi: string Base64 diekstrak dari gambar
5. String Base64 didekripsi menggunakan password → menghasilkan teks asli

### Advantages

1. **Double Security:** Kombinasi enkripsi kriptografi + steganografi
2. **Industry Standard:** Menggunakan AES-256 yang merupakan standar enkripsi
3. **Authenticated Encryption:** GCM mode memastikan integritas data
4. **Password-Based:** Tidak perlu mengelola kunci secara manual
5. **Base64 Compatible:** Output kompatibel dengan sistem steganografi existing

### Usage Example

```python
from aes_crypto import encrypt, decrypt

# Enkripsi
plaintext = "Pesan rahasia ini sangat penting!"
password = "password_yang_kuat_123"
encrypted = encrypt(plaintext, password)
print(f"Encrypted: {encrypted}")

# Dekripsi
try:
    decrypted = decrypt(encrypted, password)
    print(f"Decrypted: {decrypted}")
except ValueError as e:
    print(f"Dekripsi gagal: {e}")
```

### Security Considerations

1. **Password Strength:** Gunakan password yang kuat dan unik
2. **Key Storage:** Jangan hardcode password dalam kode
3. **Error Messages:** Error message sengaja dibuat umum untuk mencegah information leakage
4. **Iteration Count:** 100,000 iterasi cukup untuk tahun 2024, pertimbangkan peningkatan di masa depan


# PSNR PROGRAM

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

# Fitur Watermarking

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


# User Experience

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

# AES-256 Encryption Module

## Overview
Modul ini menyediakan implementasi enkripsi dan dekripsi menggunakan AES-256 dalam mode GCM (Galois/Counter Mode) dengan key derivation menggunakan PBKDF2. Modul ini dirancang khusus untuk diintegrasikan dengan sistem steganografi untuk memberikan keamanan berlapis pada pesan yang disembunyikan.

## Dependencies
```python
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
```

**Library yang dibutuhkan:**
- `pycryptodome` - Library kriptografi Python untuk operasi AES dan PBKDF2

## Configuration Constants

```python
# Konfigurasi
SALT_SIZE = 16
KEY_SIZE = 32  # AES-256
ITERATIONS = 100000
```

**Penjelasan Code:**
- **SALT_SIZE = 16:** Ukuran salt dalam bytes (128-bit) - salt digunakan untuk membuat setiap enkripsi unik
- **KEY_SIZE = 32:** Ukuran kunci AES-256 dalam bytes (256-bit) - menentukan tingkat keamanan enkripsi
- **ITERATIONS = 100000:** Jumlah iterasi PBKDF2 - semakin tinggi semakin aman tapi lambat

## Core Functions

### 1. `encrypt(plain_text: str, password: str) -> str`

```python
def encrypt(plain_text: str, password: str) -> str:
    """
    Mengenkripsi teks menggunakan AES-256 GCM dengan password.
    
    Returns:
        str: String Base64 yang berisi (salt + nonce + tag + ciphertext).
    """
    # 1. Ubah data menjadi bytes
    data = plain_text.encode('utf-8')
    
    # 2. Buat salt acak
    salt = get_random_bytes(SALT_SIZE)
    
    # 3. Turunkan kunci dari password dan salt
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS)
    
    # 4. Buat cipher AES dalam mode GCM
    cipher = AES.new(key, AES.MODE_GCM)
    
    # 5. Enkripsi data
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    # 6. Gabungkan semua komponen (salt, nonce, tag, ciphertext)
    encrypted_package = salt + cipher.nonce + tag + ciphertext
    
    # 7. Kembalikan sebagai string Base64 agar aman untuk steganografi
    return base64.b64encode(encrypted_package).decode('utf-8')
```

**Penjelasan Code:**

- **Line 7:** Mengkonversi teks input menjadi bytes UTF-8 karena AES bekerja dengan data binary
- **Line 10:** Generate salt random 16 bytes menggunakan `get_random_bytes()` untuk setiap operasi enkripsi
- **Line 13:** Menggunakan PBKDF2 untuk menghasilkan kunci AES 256-bit dari password dan salt dengan 100,000 iterasi
- **Line 16:** Membuat objek cipher AES dalam mode GCM yang memberikan enkripsi dan otentikasi sekaligus
- **Line 19:** Melakukan enkripsi dan menghasilkan ciphertext + authentication tag dalam satu operasi
- **Line 22:** Menggabungkan semua komponen dalam urutan: salt + nonce + tag + ciphertext
- **Line 25:** Mengkonversi hasil binary ke Base64 string agar kompatibel dengan steganografi

**Struktur Output:**
```
[Salt 16 bytes][Nonce 16 bytes][Tag 16 bytes][Ciphertext variable bytes] -> Base64
```

### 2. `decrypt(b64_encrypted: str, password: str) -> str`

```python
def decrypt(b64_encrypted: str, password: str) -> str:
    """
    Mendekripsi data yang dienkripsi dengan AES-256 GCM.
    
    Args:
        b64_encrypted (str): String Base64 dari fungsi encrypt.
    
    Returns:
        str: Teks asli.
        
    Raises:
        ValueError: Jika password salah atau data rusak.
    """
    try:
        # 1. Decode Base64 menjadi bytes
        encrypted_package = base64.b64decode(b64_encrypted)
        
        # 2. Ekstrak komponen dari package
        # Ukuran: salt(16), nonce(16 GCM default), tag(16 GCM default)
        salt = encrypted_package[:SALT_SIZE]
        nonce = encrypted_package[SALT_SIZE:SALT_SIZE + 16]
        tag = encrypted_package[SALT_SIZE + 16:SALT_SIZE + 32]
        ciphertext = encrypted_package[SALT_SIZE + 32:]
        
        # 3. Turunkan kunci dari password dan salt yang diekstrak
        key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS)
        
        # 4. Buat cipher dengan kunci dan nonce yang diekstrak
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        
        # 5. Dekripsi dan verifikasi data. Ini akan error jika tag tidak cocok.
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        
        # 6. Kembalikan sebagai string
        return decrypted_data.decode('utf-8')

    except (ValueError, KeyError, IndexError) as e:
        # Jika terjadi error apapun selama proses unpacking atau dekripsi,
        # kemungkinan besar password salah atau data telah rusak.
        raise ValueError("Password salah atau data korup.")
```

**Penjelasan Code:**

- **Line 14:** Decode string Base64 kembali menjadi bytes binary
- **Line 17-20:** Ekstrak komponen dengan slicing: salt (16 bytes), nonce (16 bytes), tag (16 bytes), sisanya ciphertext
- **Line 23:** Regenerate kunci yang sama menggunakan PBKDF2 dengan password dan salt yang diekstrak
- **Line 26:** Membuat cipher AES-GCM dengan kunci dan nonce yang sudah diekstrak
- **Line 29:** Dekripsi ciphertext dan verifikasi authentication tag secara bersamaan - akan throw exception jika tag tidak cocok
- **Line 32:** Konversi hasil dekripsi dari bytes kembali ke string UTF-8
- **Line 34-37:** Error handling yang menangkap semua kemungkinan error dan memberikan pesan yang konsisten untuk keamanan

## Security Features

### 1. **AES-256 GCM Mode**
- **Enkripsi:** Menggunakan AES dengan kunci 256-bit
- **Mode GCM:** Memberikan confidentiality dan authenticity sekaligus
- **Authentication Tag:** Memastikan integritas data dan deteksi tampering

### 2. **PBKDF2 Key Derivation**
- **Salt:** 16 bytes random salt untuk setiap enkripsi
- **Iterasi:** 100,000 iterasi untuk memperlambat brute force attack
- **Output:** Kunci 256-bit yang konsisten dari password yang sama

### 3. **Randomization**
- **Salt:** Unik untuk setiap operasi enkripsi
- **Nonce:** Otomatis dihasilkan oleh GCM mode untuk setiap enkripsi

