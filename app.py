import streamlit as st
from PIL import Image
from visual_crypto import create_shares, combine_shares
from stegano import encode_lsb, decode_lsb
import io

st.title("🔐 Kriptografi Visual & Steganografi")

st.header("1️⃣ Enkripsi")
secret_file = st.file_uploader("Upload secret.png (hitam-putih)", type=["png"])
cover_file = st.file_uploader("Upload cover.png (berwarna)", type=["png"])

if secret_file and cover_file:
    secret = Image.open(secret_file)
    cover = Image.open(cover_file)
    share1, share2 = create_shares(secret)
    stego = encode_lsb(cover, share2)

    st.image(share1, caption="Share 1")
    st.image(stego, caption="Cover dengan Share 2 (stego image)")

    buf1, buf2 = io.BytesIO(), io.BytesIO()
    share1.save(buf1, format="PNG")
    stego.save(buf2, format="PNG")

    st.download_button("⬇️ Download Share 1", data=buf1.getvalue(), file_name="share1.png")
    st.download_button("⬇️ Download Stego Image", data=buf2.getvalue(), file_name="cover_encoded.png")

st.header("2️⃣ Dekripsi")
share1_file = st.file_uploader("Upload share1.png", type=["png"], key="dec1")
stego_file = st.file_uploader("Upload cover_encoded.png", type=["png"], key="dec2")

if share1_file and stego_file:
    share1 = Image.open(share1_file)
    stego = Image.open(stego_file)
    share2 = decode_lsb(stego).resize(share1.size)
    result = combine_shares(share1, share2)

    st.image(result, caption="Hasil Rekonstruksi")

    buf = io.BytesIO()
    result.save(buf, format="PNG")
    st.download_button("⬇️ Download Hasil", data=buf.getvalue(), file_name="result.png")
