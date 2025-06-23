import streamlit as st
from PIL import Image
import io
import traceback
from aes_crypto import encrypt_image, decrypt_image
import base64
import zipfile

# --- BAGIAN INISIALISASI ---
SECRET_UPLOADER_KEY_BASE = "vc_secret_uploader"
SHARES_UPLOADER_KEY_BASE = "vc_shares_upload"

if 'vc_shares_list' not in st.session_state: st.session_state.vc_shares_list = None
if 'vc_result_data_color' not in st.session_state: st.session_state.vc_result_data_color = None
if 'stego_text_img_data' not in st.session_state: st.session_state.stego_text_img_data = None
if 'extracted_text_data' not in st.session_state: st.session_state.extracted_text_data = None
if 'watermarked_image_data' not in st.session_state: st.session_state.watermarked_image_data = None
if 'uploader_version' not in st.session_state: st.session_state.uploader_version = 0
if 'selected_tab' not in st.session_state: st.session_state.selected_tab = ""

def reset_vc_output_state():
    st.session_state.vc_shares_list = None
    st.session_state.vc_result_data_color = None

def reset_stego_state():
    st.session_state.stego_text_img_data = None
    st.session_state.extracted_text_data = None

def reset_wm_state():
    st.session_state.watermarked_image_data = None

def handle_tab_change(tab_name):
    if st.session_state.selected_tab != tab_name:
        reset_vc_output_state()
        reset_stego_state()
        reset_wm_state()
        st.session_state.selected_tab = tab_name

try:
    from visual_crypto import create_color_shares, combine_color_shares
    from stegano import encode_text, decode_text
    from metrics import calculate_metrics
    from watermark import add_image_watermark, add_text_watermark
except ImportError as e:
    st.error(f"Gagal mengimpor modul: {e}. Pastikan semua file .py ada.")
    st.stop()

st.set_page_config(page_title="Pusat Kriptografi & Citra", layout="wide")
st.title("🔐 Pusat Kriptografi, Steganografi & Pengolahan Citra")

tab_labels = [
    "Kriptografi Visual",
    "Steganografi Teks",
    "Analisis Kualitas (PSNR)",
    "Watermarking Visual"
]

selected_tab = st.radio("Pilih Menu", tab_labels, key="selected_tab_radio", horizontal=True)
handle_tab_change(selected_tab)

# --- Tab 1: Kriptografi Visual (Versi Baru) ---
if selected_tab == "Kriptografi Visual":
    handle_tab_change(selected_tab)
    st.header("Metode Kriptografi Visual")
    st.info("""
    Memecah gambar menjadi beberapa 'shares'. Gambar asli hanya terlihat jika SEMUA shares digabungkan.
    **Catatan:** Kualitas visual hasil rekonstruksi bersifat lossy dan tidak akan 100% identik.
    """)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("1. Buat Shares")
        
        secret_uploader_key = f"{SECRET_UPLOADER_KEY_BASE}_{st.session_state.uploader_version}"
        secret_vc_file = st.file_uploader("Upload gambar rahasia", type=["png", "bmp", "jpg", "jpeg"], key=secret_uploader_key)

        if st.session_state.get(secret_uploader_key) is not None:
            if st.button("Hapus Gambar Rahasia", key="clear_secret_vc"):
                st.session_state.uploader_version += 1
                reset_vc_output_state()
                st.rerun()

        with st.form("vc_encrypt_form_color"):
            num_shares = st.number_input("Jumlah shares yang ingin dibuat", min_value=2, max_value=10, value=2, step=1)
            submitted_create = st.form_submit_button("Buat Shares")
            if submitted_create:
                if st.session_state.get(secret_uploader_key) is not None:
                    reset_vc_output_state() 
                    try:
                        secret_img_data = st.session_state[secret_uploader_key]
                        secret_img = Image.open(secret_img_data)
                        with st.spinner(f"Membuat {num_shares} shares..."):
                            shares_list = create_color_shares(secret_img, num_shares)
                        st.session_state.vc_shares_list = shares_list
                        st.success(f"{num_shares} shares berhasil dibuat!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Harap upload gambar rahasia terlebih dahulu.")
        
        if 'vc_shares_list' in st.session_state and st.session_state.vc_shares_list:
            st.write("---"); st.subheader("Hasil Shares:")
            shares_list = st.session_state.vc_shares_list
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                for i, share_img in enumerate(shares_list):
                    st.image(share_img, caption=f"Share {i + 1}")
                    buf_individual = io.BytesIO(); share_img.save(buf_individual, format="PNG")
                    st.download_button(f"⬇️ Download Share {i + 1}", buf_individual, f"share_{i + 1}.png", "image/png", key=f"vc_dl_{i+1}")
                    buf_for_zip = io.BytesIO(); share_img.save(buf_for_zip, format="PNG")
                    zf.writestr(f"share_{i + 1}.png", buf_for_zip.getvalue())
            st.write("---")
            st.download_button(label="⬇️ Download Semua Shares (.zip)", data=zip_buffer.getvalue(), file_name="shares.zip", mime="application/zip")

    with col2:
        st.subheader("2. Gabungkan Shares")
        
        shares_uploader_key = f"{SHARES_UPLOADER_KEY_BASE}_{st.session_state.uploader_version}"
        uploaded_shares = st.file_uploader("Upload SEMUA shares", type=["png"], accept_multiple_files=True, key=shares_uploader_key)

        b_col1, b_col2 = st.columns([3, 2]) 

        with b_col1:
            if st.button("Gabungkan Shares", key="combine_button", use_container_width=True):
                if shares_uploader_key in st.session_state and st.session_state[shares_uploader_key]:
                    if len(st.session_state[shares_uploader_key]) >= 2:
                        st.session_state.vc_result_data_color = None
                        try:
                            share_images = [Image.open(f) for f in st.session_state[shares_uploader_key]]
                            with st.spinner("Menggabungkan shares..."):
                                result_image = combine_color_shares(share_images)
                            st.session_state.vc_result_data_color = result_image
                            st.success("Gambar berhasil direkonstruksi!")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.warning("Harap upload minimal 2 file share.")
                else:
                    st.warning("Harap upload file share terlebih dahulu.")
        
        with b_col2:
            if st.session_state.get(shares_uploader_key):
                if st.button("Hapus Uploads", key="clear_uploaded_shares", use_container_width=True):
                    st.session_state.uploader_version += 1
                    reset_vc_output_state()
                    st.rerun()

        if 'vc_result_data_color' in st.session_state and st.session_state.vc_result_data_color:
            st.image(st.session_state.vc_result_data_color, caption="Hasil Gabungan")
            buf = io.BytesIO(); st.session_state.vc_result_data_color.save(buf, format="PNG")
            st.download_button("⬇️ Download Hasil", buf, "reconstructed.png", "image/png", key="vc_dl_res")

# --- Tab 2: Steganografi Teks ---
elif selected_tab == "Steganografi Teks":
    handle_tab_change(selected_tab)
    st.header("Metode Steganografi Teks")
    st.info("Menyembunyikan teks rahasia di dalam gambar.")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("1. Sembunyikan Teks")
        secret_text = st.text_area("Masukkan teks rahasia:", key="steg_text_widget")
        use_password = st.radio("Gunakan Password untuk Enkripsi?", ["Tidak", "Ya"], horizontal=True)
        password = st.text_input("Masukkan Password", type="password") if use_password == "Ya" else ""
        block_size = st.selectbox("Ukuran Blok untuk Penyisipan", [1, 16, 32], index=0)
        cover_steg_file = st.file_uploader("Upload gambar sampul", type=["png", "bmp", "jpg", "jpeg"], key="steg_cover_widget")
        with st.form("steg_encrypt_form", clear_on_submit=True):
            submitted = st.form_submit_button("Sembunyikan Teks")
            if submitted and secret_text and cover_steg_file:
                try:
                    cover_img = Image.open(cover_steg_file)
                    if use_password == "Ya":
                        encrypted_bytes = encrypt_image(secret_text.encode("utf-8"), password)
                        secret_encoded = base64.b64encode(encrypted_bytes).decode("utf-8")
                    else:
                        secret_encoded = secret_text
                    st.session_state.stego_text_img_data = encode_text(cover_img, secret_encoded, block_size=block_size)
                    st.success("Teks berhasil disembunyikan!")
                except Exception as e:
                    st.error(f"Error: {e}")
    if st.session_state.stego_text_img_data:
        st.image(st.session_state.stego_text_img_data, caption="Gambar Stego")
        buf = io.BytesIO(); st.session_state.stego_text_img_data.save(buf, format="PNG")
        st.download_button("⬇️ Download Gambar Stego", buf, "stego_text.png", "image/png")
    with col2:
        st.subheader("2. Ekstrak Teks")
        use_password_extract = st.radio("Apakah Teks Dienkripsi?", ["Tidak", "Ya"], horizontal=True)
        extract_password = st.text_input("Masukkan Password Dekripsi", type="password") if use_password_extract == "Ya" else ""
        block_size_ext = st.selectbox("Ukuran Blok Ekstraksi", [1, 16, 32], index=0, key="blk_ext")
        stego_file = st.file_uploader("Upload gambar stego", type=["png", "jpg", "jpeg"], key="steg_file_widget")
        if st.button("Ekstrak Teks"):
            if stego_file:
                try:
                    stego_img = Image.open(stego_file)
                    extracted_text_raw = decode_text(stego_img, block_size=block_size_ext)
                    if use_password_extract == "Ya":
                        try:
                            encrypted_bytes = base64.b64decode(extracted_text_raw.encode("utf-8"))
                            decrypted_bytes = decrypt_image(encrypted_bytes, extract_password)
                            extracted_text = decrypted_bytes.decode('utf-8', errors='ignore')
                        except Exception as e:
                            extracted_text = f"[Gagal dekripsi]: {e}"
                    else:
                        extracted_text = extracted_text_raw
                    st.session_state.extracted_text_data = extracted_text
                    st.success("Teks berhasil diekstrak!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Silakan upload gambar stego terlebih dahulu.")
    if st.session_state.extracted_text_data is not None:
        st.text_area("Teks Rahasia:", value=st.session_state.extracted_text_data, height=200, disabled=True)

# --- Tab 3: Kalkulator PSNR (DIPERBARUI) ---
elif selected_tab == "Analisis Kualitas (PSNR)":
    handle_tab_change(selected_tab)
    st.header("Analisis Kualitas Gambar (PSNR, MSE & Skor Kemiripan)")
    st.info("""
    Menganalisis perbedaan antara gambar asli dan gambar hasil olahan menggunakan tiga metrik utama:
    - **Skor Kemiripan:** Representasi linear dari 0-100% seberapa identik kedua gambar.
    - **PSNR (Standar):** Metrik logaritmik standar industri. Semakin tinggi nilainya, semakin baik kualitasnya.
    - **MSE (Error):** Rata-rata error per piksel. Semakin rendah nilainya, semakin baik.
    """)
    st.subheader("Panduan Interpretasi Nilai PSNR")
    st.markdown("""
    - **∞ (Tak Terhingga):** :green[**Sempurna.**] Gambar 100% identik.
    - **> 40 dB:** :green[**Istimewa.**] Kualitas sangat tinggi, perbedaan hampir tidak mungkin dilihat oleh mata manusia.
    - **30 - 40 dB:** :blue[**Baik.**] Kualitas dapat diterima, namun perbedaan mungkin terlihat jika diamati teliti.
    - **< 30 dB:** :orange[**Cukup/Kurang.**] Perbedaan atau distorsi mulai terlihat jelas.
    """)
    with st.expander("ℹ️ Kenapa tidak bisa menghitung PSNR untuk hasil Kriptografi Visual?"):
        st.write("""
        Metode Kriptografi Visual memperluas setiap piksel asli menjadi blok piksel yang lebih besar. Akibatnya, resolusi gambar hasil gabungan menjadi lebih besar dari aslinya, sehingga perbandingan piksel-demi-piksel tidak dapat dilakukan.
        """)

    with st.form("psnr_form"):
        col1, col2 = st.columns(2)
        with col1:
            original_file = st.file_uploader("1. Upload Gambar Asli (Cover)", type=["png", "bmp", "jpg", "jpeg"])
        with col2:
            stego_file = st.file_uploader("2. Upload Gambar Hasil Olahan", type=["png", "bmp", "jpg", "jpeg"])
        
        submitted = st.form_submit_button("Hitung Metrik Kualitas")
        
        if submitted and original_file and stego_file:
            try:
                original_img = Image.open(original_file)
                stego_img = Image.open(stego_file)
                
                if original_img.size != stego_img.size:
                    st.error(f"**Ukuran Gambar Tidak Cocok!**\n- Gambar Asli: {original_img.size}\n- Gambar Hasil: {stego_img.size}")
                else:
                    img_col1, img_col2 = st.columns(2)
                    img_col1.image(original_img, caption="Gambar Asli", use_container_width=True)
                    img_col2.image(stego_img, caption="Gambar Hasil Olahan", use_container_width=True)
                    
                    with st.spinner("Menghitung metrik..."):
                        metrics = calculate_metrics(original_img, stego_img)
                        psnr_value = metrics['psnr']
                        mse_value = metrics['mse']
                        similarity = metrics['similarity_score']
                    
                    st.success("Perhitungan Selesai!")
                    
                    # Tampilkan 3 metrik dalam 3 kolom
                    res_col1, res_col2, res_col3 = st.columns(3)
                    with res_col1:
                        st.metric(label="Skor Kemiripan", value=f"{similarity:.2f} %", help="Skor 100% berarti gambar identik.")
                    with res_col2:
                        if psnr_value == float('inf'):
                            psnr_display = "∞ (Identik)"
                        else:
                            psnr_display = f"{psnr_value:.2f} dB"
                    st.metric(label="PSNR (Standar)", value=psnr_display, help="Semakin tinggi semakin baik. > 40 dB dianggap istimewa.")
                    with res_col3:
                        st.metric(label="MSE (Error)", value=f"{mse_value:.4f}", help="Semakin rendah semakin baik. 0 berarti sempurna.")

                    # --- LOGIKA INTERPRETASI YANG DISERDEHANAKAN DAN KONSISTEN ---
                    if psnr_value == float('inf'):
                        st.balloons()
                        st.markdown("#### Kualitas: :green[Sempurna]")
                    elif psnr_value > 40:
                        st.markdown("#### Kualitas: :green[Istimewa]")
                    elif psnr_value > 30:
                        st.markdown("#### Kualitas: :blue[Baik]")
                    else:
                        st.markdown("#### Kualitas: :orange[Cukup/Kurang]")

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
        elif submitted:
            st.warning("Harap unggah kedua gambar.")

# --- Tab 4: Watermarking ---
elif selected_tab == "Watermarking Visual":
    handle_tab_change(selected_tab)
    st.header("Watermarking Visual")
    st.info("Sisipkan logo atau teks transparan ke dalam gambar Anda untuk menandai kepemilikan.")
    base_file = st.file_uploader("1. Upload Gambar Utama", type=["png", "bmp", "jpg", "jpeg"], key="wm_base_widget")
    if base_file:
        watermark_type = st.radio("2. Pilih Jenis Watermark", options=["Gambar Logo", "Teks"], horizontal=True, key="wm_type_widget")
        st.write("---")
        if watermark_type == "Gambar Logo":
            with st.form("watermark_image_form"):
                logo_file = st.file_uploader("Upload Gambar Logo/Watermark", type=["png", "bmp", "jpg", "jpeg"], key="wm_logo_widget")
                st.subheader("Pengaturan Watermark Gambar:")
                col1, col2 = st.columns(2)
                with col1: opacity_img = st.slider("Tingkat Opacity", 0.1, 1.0, 0.5, 0.05, key="img_opacity")
                with col2: scale_img = st.slider("Ukuran Relatif", 0.05, 0.5, 0.15, 0.01, key="img_scale")
                position_img = st.selectbox("Posisi", ['bottom-right', 'bottom-left', 'top-right', 'top-left', 'center'], index=0, key="img_pos")
                submitted = st.form_submit_button("Tambahkan Watermark Gambar")
                if submitted and logo_file:
                    try:
                        base_img = Image.open(base_file)
                        logo_img = Image.open(logo_file)
                        with st.spinner("Memproses..."):
                            watermarked_img = add_image_watermark(base_img, logo_img, position_img, opacity_img, scale_img)
                            st.session_state.watermarked_image_data = watermarked_img
                            st.success("Watermark gambar berhasil ditambahkan!")
                    except Exception as e: st.error(f"Terjadi kesalahan: {e}")
        elif watermark_type == "Teks":
            with st.form("watermark_text_form"):
                watermark_text = st.text_input("Masukkan Teks Watermark", "© Nama Anda 2024")
                st.subheader("Pengaturan Watermark Teks:")
                col1, col2, col3 = st.columns(3)
                with col1: font_size_txt = st.slider("Ukuran Font", 10, 200, 50, key="txt_size")
                with col2: opacity_txt = st.slider("Tingkat Opacity", 0.1, 1.0, 0.7, 0.05, key="txt_opacity")
                with col3: font_color_txt = st.color_picker("Warna Font", "#FFFFFF")
                position_txt = st.selectbox("Posisi", ['bottom-right', 'bottom-left', 'top-right', 'top-left', 'center'], index=0, key="txt_pos")
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
                    except Exception as e: st.error(f"Terjadi kesalahan: {e}")
        if 'watermarked_image_data' in st.session_state and st.session_state.watermarked_image_data:
            st.image(st.session_state.watermarked_image_data, caption="Gambar Hasil Watermark", use_column_width=True)
            buf = io.BytesIO()
            st.session_state.watermarked_image_data.save(buf, format="PNG")
            st.download_button(label="⬇️ Download Gambar Hasil", data=buf, file_name="watermarked_image.png", mime="image/png", key="dl_wm_widget")