import streamlit as st
from PIL import Image
from visual_crypto import create_shares, combine_shares
from stegano import encode_lsb, decode_lsb
from aes_crypto import encrypt_image, decrypt_image
from watermark import add_watermark
from psnr_util import calculate_psnr
import io

st.set_page_config(page_title="🛡 Kriptografi Media Suite", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #f5faff;
        color: #0a2a66;
    }
    .stButton>button, .stDownloadButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 8px;
        padding: 0.4rem 1.2rem;
        font-weight: 600;
    }
    .stTextInput>div>input {
        border: 1px solid #4a90e2;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧩 Kriptografi Visual, Steganografi, AES, Watermark + PSNR")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔐 Visual + Stegano", "🕵‍♂ Dekripsi", "🖋 Watermark", "🛡 AES Encrypt/Decrypt", "📊 PSNR Quality"
])

with tab1:
    st.subheader("🔐 Enkripsi Gambar Visual + Steganografi")
    secret_file = st.file_uploader("📥 Gambar Rahasia (BW)", type=["png"], key="vs1")
    cover_file = st.file_uploader("📥 Cover Image (RGB)", type=["png"], key="vs2")
    if secret_file and cover_file:
        try:
            secret = Image.open(secret_file)
            cover = Image.open(cover_file)
            share1, share2 = create_shares(secret)
            stego = encode_lsb(cover, share2)

            col1, col2 = st.columns(2)
            with col1:
                st.image(share1, caption="🖼 Share 1", use_container_width=True)
                buf1 = io.BytesIO()
                share1.save(buf1, format="PNG")
                st.download_button("⬇ Unduh Share 1", buf1.getvalue(), file_name="share1.png")
            with col2:
                st.image(stego, caption="🖼 Stego Image", use_container_width=True)
                buf2 = io.BytesIO()
                stego.save(buf2, format="PNG")
                st.download_button("⬇ Unduh Stego Image", buf2.getvalue(), file_name="cover_encoded.png")

            psnr = calculate_psnr(cover, stego)
            st.metric("📊 PSNR (Cover vs Stego)", f"{psnr:.2f} dB", help="Semakin tinggi PSNR, semakin mirip.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with tab2:
    st.subheader("🕵‍♂ Dekripsi Gambar dari Share + Stego")
    share1_file = st.file_uploader("📥 Upload Share 1", type=["png"], key="d1")
    stego_file = st.file_uploader("📥 Upload Stego Image", type=["png"], key="d2")
    if share1_file and stego_file:
        try:
            share1 = Image.open(share1_file).convert('1')
            stego = Image.open(stego_file).convert('RGB')

            share2 = decode_lsb(stego).resize(share1.size)
            st.image(share2, caption="🔍 Share 2 (Hasil Ekstraksi)", use_container_width=True)

            result = combine_shares(share1, share2)
            st.image(result, caption="📄 Hasil Rekonstruksi", use_container_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button("⬇ Unduh Gambar Terdekripsi", buf.getvalue(), file_name="decrypted.png")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with tab3:
    st.subheader("🖋 Tambahkan Watermark ke Gambar")
    wm_file = st.file_uploader("📥 Upload Gambar", type=["png", "jpg", "jpeg"], key="wm")
    watermark_text = st.text_input("✍ Teks Watermark (Contoh: Nama/NIM/Kelas)")
    if wm_file and watermark_text:
        try:
            img = Image.open(wm_file)
            watermarked = add_watermark(img, watermark_text)
            st.image(watermarked, caption="📌 Gambar dengan Watermark", use_container_width=True)
            buf = io.BytesIO()
            watermarked.save(buf, format="PNG")
            st.download_button("⬇ Unduh Gambar Watermark", buf.getvalue(), file_name="watermarked.png")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with tab4:
    st.subheader("🛡 Enkripsi & Dekripsi Gambar menggunakan AES")

    if "aes_mode" not in st.session_state:
        st.session_state.aes_mode = "🔐 Enkripsi"

    mode = st.radio("📤 Pilih Mode:", ["🔐 Enkripsi", "🔓 Dekripsi"], horizontal=True,
                    index=0 if st.session_state.aes_mode == "🔐 Enkripsi" else 1)
    if mode != st.session_state.aes_mode:
        st.session_state.aes_mode = mode
        st.experimental_rerun()

    aes_key = st.text_input("🔑 Password AES", type="password")
    aes_file = st.file_uploader("📥 Upload Gambar (.png) atau File Enkripsi (.enc)",
                                type=["png", "enc"], key=st.session_state.aes_mode)

    if aes_file and aes_key:
        try:
            if st.session_state.aes_mode == "🔐 Enkripsi":
                img = Image.open(aes_file)
                encrypted = encrypt_image(img, aes_key)
                st.success("✅ Enkripsi berhasil.")
                st.download_button("⬇ Unduh File Terenkripsi", encrypted, file_name="encrypted.enc")
            else:
                raw = aes_file.read()
                decrypted_img = decrypt_image(raw, aes_key)
                st.success("✅ Dekripsi berhasil.")
                st.image(decrypted_img, caption="📄 Gambar Terdekripsi", use_container_width=True)
                buf = io.BytesIO()
                decrypted_img.save(buf, format="PNG")
                st.download_button("⬇ Unduh Gambar Hasil", buf.getvalue(), file_name="decrypted_aes.png")
        except Exception as e:
            st.error("❌ Gagal mendekripsi. Coba periksa password dan file!")

with tab5:
    st.subheader("📊 Bandingkan 2 Gambar (Manual PSNR)")
    img1 = st.file_uploader("Gambar Asli", type=["png"], key="ps1")
    img2 = st.file_uploader("Gambar Bandingan", type=["png"], key="ps2")
    if img1 and img2:
        try:
            im1 = Image.open(img1)
            im2 = Image.open(img2)
            score = calculate_psnr(im1, im2)
            st.metric("📈 PSNR Nilai", f"{score:.2f} dB")
        except Exception as e:
            st.error(f"❌ Gagal menghitung PSNR: {str(e)}")
