# app.py (VERSI SEDERHANA TANPA METODE KOMBINASI)

import streamlit as st
from PIL import Image
import io
import traceback

# --- BAGIAN INISIALISASI ---

# Inisialisasi session state dengan kunci unik untuk DATA
# Kunci untuk Kripto Visual
if 'vc_share1_data' not in st.session_state: st.session_state.vc_share1_data = None
if 'vc_share2_data' not in st.session_state: st.session_state.vc_share2_data = None
if 'vc_result_data' not in st.session_state: st.session_state.vc_result_data = None
# Kunci untuk Stegano Teks
if 'stego_text_img_data' not in st.session_state: st.session_state.stego_text_img_data = None
if 'extracted_text_data' not in st.session_state: st.session_state.extracted_text_data = None
# Kunci untuk Watermark
if 'watermarked_image_data' not in st.session_state: st.session_state.watermarked_image_data = None


# Impor fungsi dari file lokal
try:
    # Hanya impor yang diperlukan
    from visual_crypto import create_shares, combine_shares
    from stegano import encode_text, decode_text
    from metrics import calculate_psnr
    from watermark import add_image_watermark, add_text_watermark
except ImportError as e:
    st.error(f"Gagal mengimpor modul: {e}. Pastikan file 'visual_crypto.py', 'stegano.py', 'metrics.py', dan 'watermark.py' ada di folder yang sama.")
    st.stop()


# --- BAGIAN UI (ANTARMUKA) ---

# Konfigurasi Halaman
st.set_page_config(page_title="Pusat Kriptografi & Citra", layout="wide")
st.title("🔐 Pusat Kriptografi, Steganografi & Pengolahan Citra")

# Membuat Pilihan Metode Menggunakan Tabs (struktur baru 4 tab)
tab1, tab2, tab3, tab4 = st.tabs([
    "Kriptografi Visual", 
    "Steganografi Teks",
    "Analisis Kualitas (PSNR)",
    "Watermarking Visual"
])


# --- Tab 1: Kriptografi Visual ---
with tab1:
    st.header("Metode Kriptografi Visual")
    st.info("Memecah satu gambar rahasia menjadi dua gambar acak (shares). Gambar asli hanya bisa dilihat dengan menggabungkan kedua shares.")
    
    col1, col2 = st.columns(2, gap="large")
    
    # Enkripsi VC
    with col1:
        st.subheader("1. Buat Shares (Enkripsi)")
        with st.form("vc_encrypt_form", clear_on_submit=True):
            secret_vc_file = st.file_uploader("Upload gambar rahasia (hitam-putih)", type=["png", "bmp"], key="vc_secret_widget")
            submitted = st.form_submit_button("Buat Shares")
            if submitted and secret_vc_file:
                try:
                    secret_img = Image.open(secret_vc_file)
                    st.session_state.vc_share1_data, st.session_state.vc_share2_data = create_shares(secret_img)
                    st.success("Shares berhasil dibuat! Hasil ditampilkan di bawah.")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        if st.session_state.vc_share1_data and st.session_state.vc_share2_data:
            st.image(st.session_state.vc_share1_data, caption="Share 1")
            buf1 = io.BytesIO()
            st.session_state.vc_share1_data.save(buf1, format="PNG")
            st.download_button("⬇️ Download Share 1", buf1, "share1.png", "image/png", key="vc_dl1_widget")

            st.image(st.session_state.vc_share2_data, caption="Share 2")
            buf2 = io.BytesIO()
            st.session_state.vc_share2_data.save(buf2, format="PNG")
            st.download_button("⬇️ Download Share 2", buf2, "share2.png", "image/png", key="vc_dl2_widget")

    # Dekripsi VC
    with col2:
        st.subheader("2. Gabungkan Shares (Dekripsi)")
        with st.form("vc_decrypt_form", clear_on_submit=True):
            share1_file = st.file_uploader("Upload Share 1", type=["png"], key="vc_share1_widget")
            share2_file = st.file_uploader("Upload Share 2", type=["png"], key="vc_share2_widget")
            submitted = st.form_submit_button("Gabungkan Shares")
            if submitted and share1_file and share2_file:
                try:
                    share1_img = Image.open(share1_file)
                    share2_img = Image.open(share2_file)
                    st.session_state.vc_result_data = combine_shares(share1_img, share2_img)
                    st.success("Gambar berhasil direkonstruksi! Hasil ditampilkan di bawah.")
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state.vc_result_data:
            st.image(st.session_state.vc_result_data, caption="Hasil Gabungan")
            buf = io.BytesIO()
            st.session_state.vc_result_data.save(buf, format="PNG")
            st.download_button("⬇️ Download Hasil", buf, "result_vc.png", "image/png", key="vc_dl_res_widget")


# --- Tab 2: Steganografi Teks ---
with tab2:
    st.header("Metode Steganografi Teks")
    st.info("Menyembunyikan pesan teks rahasia di dalam gambar sampul dan mengekstraknya kembali.")
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("1. Sembunyikan Teks (Enkripsi)")
        with st.form("steg_encrypt_form", clear_on_submit=True):
            secret_text = st.text_area("Masukkan teks rahasia di sini:", key="steg_text_widget")
            cover_steg_file = st.file_uploader("Upload gambar sampul", type=["png", "bmp", "jpg", "jpeg"], key="steg_cover_widget")
            submitted = st.form_submit_button("Sembunyikan Teks")
            if submitted and secret_text and cover_steg_file:
                try:
                    cover_img = Image.open(cover_steg_file)
                    st.session_state.stego_text_img_data = encode_text(cover_img, secret_text)
                    st.success("Teks berhasil disembunyikan!")
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state.stego_text_img_data:
            st.image(st.session_state.stego_text_img_data, caption="Gambar Stego (dengan teks tersembunyi)")
            buf = io.BytesIO()
            st.session_state.stego_text_img_data.save(buf, format="PNG")
            st.download_button("⬇️ Download Gambar Stego", buf, "stego_text.png", "image/png", key="steg_dl_widget")

    with col2:
        st.subheader("2. Ekstrak Teks (Dekripsi)")
        with st.form("steg_decrypt_form", clear_on_submit=True):
            stego_file = st.file_uploader("Upload gambar stego", type=["png", "jpg", "jpeg"], key="steg_file_widget")
            submitted = st.form_submit_button("Ekstrak Teks")
            if submitted and stego_file:
                try:
                    stego_img = Image.open(stego_file)
                    st.session_state.extracted_text_data = decode_text(stego_img)
                    st.success("Teks berhasil diekstrak!")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        if st.session_state.extracted_text_data is not None:
            st.text_area("Teks Rahasia:", value=st.session_state.extracted_text_data, height=200, disabled=True, key="steg_res_widget")


# --- Tab 3: Kalkulator PSNR ---
with tab3:
    st.header("Analisis Kualitas Gambar (PSNR)")
    st.info("""
    PSNR (Peak Signal-to-Noise Ratio) digunakan untuk mengukur seberapa mirip sebuah gambar hasil olahan
    (misal: stego-image) dengan gambar aslinya (cover-image).
    - **Nilai > 35 dB:** Perbedaan hampir tidak mungkin dilihat. Kualitas sangat baik.
    - **Nilai 30-35 dB:** Perbedaan mungkin terlihat jika diperhatikan dengan sangat teliti. Kualitas baik.
    - **Nilai < 30 dB:** Perbedaan mulai terlihat.
    """)
    
    with st.form("psnr_form"):
        original_file = st.file_uploader("1. Upload Gambar Asli (Cover)", type=["png", "bmp", "jpg", "jpeg"])
        stego_file = st.file_uploader("2. Upload Gambar Hasil Steganografi (Stego)", type=["png", "bmp", "jpg", "jpeg"])
        
        submitted = st.form_submit_button("Hitung PSNR")
        
        if submitted and original_file and stego_file:
            try:
                original_img = Image.open(original_file).convert("RGB")
                stego_img = Image.open(stego_file).convert("RGB")
                
                if original_img.size != stego_img.size:
                    st.error("Error: Ukuran kedua gambar harus sama untuk menghitung PSNR.")
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(original_img, caption="Gambar Asli", use_column_width=True)
                    with col2:
                        st.image(stego_img, caption="Gambar Stego", use_column_width=True)
                    
                    with st.spinner("Menghitung PSNR..."):
                        psnr_value = calculate_psnr(original_img, stego_img)
                        st.success(f"**Nilai PSNR: {psnr_value:.2f} dB**")

                        if psnr_value > 35:
                            st.balloons()
                            st.markdown("#### Kualitas: :green[Sangat Baik]")
                        elif psnr_value > 30:
                            st.markdown("#### Kualitas: :blue[Baik]")
                        else:
                            st.markdown("#### Kualitas: :orange[Cukup (Perbedaan mungkin terlihat)]")
                        
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")


# --- Tab 4: Watermarking ---
with tab4:
    st.header("Watermarking Visual")
    st.info("Sisipkan logo atau teks transparan ke dalam gambar Anda untuk menandai kepemilikan.")

    base_file = st.file_uploader("1. Upload Gambar Utama", type=["png", "bmp", "jpg", "jpeg"], key="wm_base_widget")

    if base_file:
        watermark_type = st.radio(
            "2. Pilih Jenis Watermark",
            options=["Gambar Logo", "Teks"],
            horizontal=True, key="wm_type_widget"
        )
        st.write("---")
        
        # OPSI WATERMARK GAMBAR
        if watermark_type == "Gambar Logo":
            with st.form("watermark_image_form"):
                logo_file = st.file_uploader(
                    "Upload Gambar Logo/Watermark",
                    type=["png", "bmp", "jpg", "jpeg"], key="wm_logo_widget"
                )
                
                st.subheader("Pengaturan Watermark Gambar:")
                col1, col2 = st.columns(2)
                with col1:
                    opacity_img = st.slider("Tingkat Opacity", 0.1, 1.0, 0.5, 0.05, key="img_opacity")
                with col2:
                    scale_img = st.slider("Ukuran Relatif", 0.05, 0.5, 0.15, 0.01, key="img_scale")
                
                position_img = st.selectbox(
                    "Posisi",
                    ['bottom-right', 'bottom-left', 'top-right', 'top-left', 'center'],
                    index=0, key="img_pos"
                )
                
                submitted = st.form_submit_button("Tambahkan Watermark Gambar")

                if submitted and logo_file:
                    try:
                        base_img = Image.open(base_file)
                        logo_img = Image.open(logo_file)
                        with st.spinner("Memproses..."):
                            watermarked_img = add_image_watermark(base_img, logo_img, position_img, opacity_img, scale_img)
                            st.session_state.watermarked_image_data = watermarked_img
                            st.success("Watermark gambar berhasil ditambahkan!")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")

        # OPSI WATERMARK TEKS
        elif watermark_type == "Teks":
            with st.form("watermark_text_form"):
                watermark_text = st.text_input("Masukkan Teks Watermark", "© Nama Anda 2024")
                
                st.subheader("Pengaturan Watermark Teks:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    font_size_txt = st.slider("Ukuran Font", 10, 200, 50, key="txt_size")
                with col2:
                    opacity_txt = st.slider("Tingkat Opacity", 0.1, 1.0, 0.7, 0.05, key="txt_opacity")
                with col3:
                    font_color_txt = st.color_picker("Warna Font", "#FFFFFF")

                position_txt = st.selectbox(
                    "Posisi",
                    ['bottom-right', 'bottom-left', 'top-right', 'top-left', 'center'],
                    index=0, key="txt_pos"
                )
                
                submitted = st.form_submit_button("Tambahkan Watermark Teks")

                if submitted and watermark_text:
                    try:
                        base_img = Image.open(base_file)
                        hex_color = font_color_txt.lstrip('#')
                        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

                        with st.spinner("Memproses..."):
                            watermarked_img = add_text_watermark(base_img, watermark_text, position_txt, opacity_txt, font_size_txt, rgb_color)
                            st.session_state.watermarked_image_data = watermarked_img
                            st.success("Watermark teks berhasil ditambahkan!")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")

        # Tampilkan hasil di luar form
        if st.session_state.watermarked_image_data:
            st.image(st.session_state.watermarked_image_data, caption="Gambar Hasil Watermark", use_column_width=True)
            
            buf = io.BytesIO()
            st.session_state.watermarked_image_data.save(buf, format="PNG")
            st.download_button(
                label="⬇️ Download Gambar Hasil",
                data=buf,
                file_name="watermarked_image.png",
                mime="image/png",
                key="dl_wm_widget"
            )